import base64
import hashlib
import hmac
import json
import os
import uuid
from urllib.request import Request, urlopen

from flask import flash, redirect, request, session, url_for
from flask_login import current_user

BASE = os.environ.get("SKIPCASH_BASE", "https://skipcashtest.azurewebsites.net")
KEY_ID = os.environ.get("SKIPCASH_KEY_ID", "a9605ac9-6272-436a-a63d-8cc6ccb26390")
SECRET = os.environ.get(
    "SKIPCASH_SECRET",
    "Nu4VP/yQnM5/O6yVz0fGlcozfhtMHQ4XAS7+6CpP95uWp41xVxRn+Pv6JLuP7dtkrPYezF6K5wQ9dFkhe6gnALPIUoYBU4LvHFWHg5iMqpKYG+yB9T1zzoyK/N8wjhUwjhVTWd/qRbx7KjpcuI654Jl4SHf4XGMYyhqOoBzYVgXGIJZviOQ9KK52SP8NrQG+NphOOChZ1NDBoZF+uoBjvDCBs+wyMJOJ4EO98y8GY5DD4w4wotSDABYGx1QsE7R97LZgGUbwsoE6VPDRZdSsFt9PjDhF9DlHLEJKd/pVsjRnDh86V0iEqMf4jSAHt3Eav+tlTbqBDuM1j8jqM+hOd3ucyobAmGNGWzFZjc10ijcfm/o3Hl1R0UBPwUmZ6qu3gL+iQxYXN3LKQPC50OCNl9+UI8qV7PCsvdKIsmcXFBhq2hWHX546yi/GhZ6EjXg5T2DkduMWesBZC9SbkiXgRI+N+exDc7e0tIMfMdxCNdeD0GHTfwZJHxQGP4+wkniB8cNdrNyzyizFagEnq+WTpA==",
)
SIGN_FIELDS = [
    "Uid",
    "KeyId",
    "Amount",
    "FirstName",
    "LastName",
    "Phone",
    "Email",
    "Street",
    "City",
    "State",
    "Country",
    "PostalCode",
    "TransactionId",
    "Custom1",
]


def _sign(body):
    combined = ",".join(f"{k}={body[k]}" for k in SIGN_FIELDS if body.get(k))
    digest = hmac.new(SECRET.encode(), combined.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def _cart_amount():
    from models import CartItem, Product

    total = 0.0
    if getattr(current_user, "is_authenticated", False):
        for row in CartItem.query.filter_by(user_id=current_user.id).all():
            if row.product:
                total += float(row.product.price) * int(row.quantity)
    else:
        cart = session.get("cart") or {}
        if cart:
            ids = [int(i) for i in cart.keys()]
            products = Product.query.filter(Product.id.in_(ids)).all() if ids else []
            by_id = {p.id: p for p in products}
            for pid, qty in cart.items():
                p = by_id.get(int(pid))
                if p:
                    total += float(p.price) * int(qty)
    coupon = session.get("coupon")
    if coupon == "FLASH10" and total:
        total = total * 0.9
    return round(total, 2)


def create_payment(amount, first, last, phone, email, street="", city="Doha", order_id=""):
    uid = str(uuid.uuid4())
    phone = (phone or "+97450000000").replace(" ", "")
    if phone and not phone.startswith("+"):
        phone = "+974" + phone.lstrip("0")
    email = email or f"{phone.replace('+','')}@1111.local"
    body = {
        "Uid": uid,
        "KeyId": KEY_ID,
        "Amount": f"{float(amount):.2f}",
        "FirstName": (first or "Guest")[:60],
        "LastName": (last or "Customer")[:60],
        "Phone": phone[:15],
        "Email": email[:255],
        "Street": (street or "Doha")[:60],
        "City": (city or "Doha")[:40],
        "Country": "QA",
        "TransactionId": (order_id or uid.replace("-", ""))[:40],
        "Custom1": order_id or uid,
        "Subject": "11-11 order",
        "Description": "11-11 marketplace sandbox payment",
        "ReturnUrl": request.url_root.rstrip("/") + "/pay/skipcash/return",
        "WebhookUrl": request.url_root.rstrip("/") + "/pay/skipcash/webhook",
    }
    payload = json.dumps(body).encode()
    req = Request(
        BASE + "/api/v1/payments",
        data=payload,
        headers={"Content-Type": "application/json", "Authorization": _sign(body)},
        method="POST",
    )
    with urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    return data.get("resultObj") or {}


def install_skipcash(app):
    if getattr(app, "_skipcash", False):
        return
    app._skipcash = True

    @app.route("/pay/skipcash", methods=["POST"])
    def pay_skipcash():
        amount = _cart_amount()
        if amount <= 0:
            flash("Your cart is empty.", "danger")
            return redirect(url_for("cart"))
        name = (request.form.get("name") or "Guest Customer").strip()
        parts = name.split(" ", 1)
        first, last = parts[0], parts[1] if len(parts) > 1 else "Customer"
        try:
            result = create_payment(
                amount,
                first,
                last,
                request.form.get("phone") or "",
                getattr(current_user, "email", None) or request.form.get("email") or "",
                request.form.get("address") or "",
                request.form.get("city") or "Doha",
                str(uuid.uuid4())[:12],
            )
        except Exception as exc:
            flash("SkipCash error: %s" % exc, "danger")
            return redirect(url_for("checkout"))
        pay_url = result.get("payUrl")
        if not pay_url:
            flash("SkipCash did not return a payment link.", "danger")
            return redirect(url_for("checkout"))
        session["skipcash_id"] = result.get("id")
        return redirect(pay_url)

    @app.route("/pay/skipcash/return")
    def pay_skipcash_return():
        flash("Payment submitted with SkipCash sandbox. Check the merchant portal for status.", "success")
        return redirect(url_for("index"))

    @app.route("/pay/skipcash/webhook", methods=["POST"])
    def pay_skipcash_webhook():
        return {"ok": True}, 200
