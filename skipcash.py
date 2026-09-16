import base64
import hashlib
import hmac
import json
import os
import secrets
import uuid
from urllib.request import Request, urlopen

from flask import flash, redirect, request, session, url_for
from flask_login import current_user, login_required

BASE = os.environ.get("SKIPCASH_BASE", "https://skipcashtest.azurewebsites.net")
KEY_ID = os.environ.get("SKIPCASH_KEY_ID", "a9605ac9-6272-436a-a63d-8cc6ccb26390")
SECRET = os.environ.get(
    "SKIPCASH_SECRET",
    "Nu4VP/yQnM5/O6yVz0fGlcozfhtMHQ4XAS7+6CpP95uWp41xVxRn+Pv6JLuP7dtkrPYezF6K5wQ9dFkhe6gnALPIUoYBU4LvHFWHg5iMqpKYG+yB9T1zzoyK/N8wjhUwjhVTWd/qRbx7KjpcuI654Jl4SHf4XGMYyhqOoBzYVgXGIJZviOQ9KK52SP8NrQG+NphOOChZ1NDBoZF+uoBjvDCBs+wyMJOJ4EO98y8GY5DD4w4wotSDABYGx1QsE7R97LZgGUbwsoE6VPDRZdSsFt9PjDhF9DlHLEJKd/pVsjRnDh86V0iEqMf4jSAHt3Eav+tlTbqBDuM1j8jqM+hOd3ucyobAmGNGWzFZjc10ijcfm/o3Hl1R0UBPwUmZ6qu3gL+iQxYXN3LKQPC50OCNl9+UI8qV7PCsvdKIsmcXFBhq2hWHX546yi/GhZ6EjXg5T2DkduMWesBZC9SbkiXgRI+N+exDc7e0tIMfMdxCNdeD0GHTfwZJHxQGP4+wkniB8cNdrNyzyizFagEnq+WTpA==",
)
SIGN_FIELDS = ["Uid", "KeyId", "Amount", "FirstName", "LastName", "Phone", "Email", "Street", "City", "State", "Country", "PostalCode", "TransactionId", "Custom1"]


def _sign(body):
    combined = ",".join(f"{k}={body[k]}" for k in SIGN_FIELDS if body.get(k))
    digest = hmac.new(SECRET.encode(), combined.encode(), hashlib.sha256).digest()
    return base64.b64encode(digest).decode()


def create_payment(amount, first, last, phone, email, street, city, order_no):
    uid = str(uuid.uuid4())
    phone = (phone or "+97450000000").replace(" ", "")
    if phone and not phone.startswith("+"):
        phone = "+974" + phone.lstrip("0")
    email = email or f"{phone.replace('+','')}@1111.local"
    root = request.url_root.rstrip("/")
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
        "TransactionId": order_no.replace("-", "")[:40],
        "Custom1": order_no,
        "Subject": "11-11 %s" % order_no,
        "Description": "11-11 order %s" % order_no,
        "ReturnUrl": root + "/pay/skipcash/return?order=" + order_no,
        "WebhookUrl": root + "/pay/skipcash/webhook",
    }
    req = Request(
        BASE + "/api/v1/payments",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": _sign(body)},
        method="POST",
    )
    with urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    return data.get("resultObj") or {}


def _mark_paid(order):
    from extensions import db
    order.status = "paid"
    order.payment_method = "skipcash"
    db.session.commit()


def install_skipcash(app):
    if getattr(app, "_skipcash", False):
        return
    app._skipcash = True
    from extensions import db
    from models import CartItem, Order, OrderItem, Product

    @app.route("/pay/skipcash", methods=["POST"])
    @login_required
    def pay_skipcash():
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        rows = []
        for it in items:
            if it.product:
                rows.append((it.product, int(it.quantity)))
        if not rows:
            guest = session.get("cart") or {}
            ids = [int(k) for k in guest.keys()] if guest else []
            found = {p.id: p for p in Product.query.filter(Product.id.in_(ids)).all()} if ids else {}
            for pid, qty in guest.items():
                p = found.get(int(pid))
                if p:
                    rows.append((p, int(qty)))
        if not rows:
            flash("Your cart is empty.", "danger")
            return redirect(url_for("cart"))
        subtotal = sum(p.price * q for p, q in rows)
        shipping = 0 if subtotal >= 200 else 25
        discount = round(subtotal * 0.10, 2) if session.get("coupon") == "FLASH10" else 0
        total = max(0, subtotal + shipping - discount)
        name = (request.form.get("name") or current_user.name or "Customer").strip()
        phone = (request.form.get("phone") or current_user.phone or "50000000").strip()
        address = (request.form.get("address") or "Doha").strip()
        city = (request.form.get("city") or "Doha").strip()
        parts = name.split(" ", 1)
        order_no = "1111-" + secrets.token_hex(4).upper()
        order = Order(
            user_id=current_user.id,
            order_number=order_no,
            status="pending",
            payment_method="skipcash",
            subtotal=subtotal,
            shipping=shipping,
            total=total,
            shipping_name=name,
            shipping_phone=phone,
            shipping_address=address,
            shipping_city=city,
            note=request.form.get("note") or "",
        )
        db.session.add(order)
        db.session.flush()
        for p, q in rows:
            db.session.add(OrderItem(order_id=order.id, product_id=p.id, name=p.name, price=p.price, quantity=q, image=p.image))
            p.sold = (p.sold or 0) + q
            p.stock = max(0, (p.stock or 0) - q)
        CartItem.query.filter_by(user_id=current_user.id).delete()
        session["cart"] = {}
        db.session.commit()
        try:
            result = create_payment(total, parts[0], parts[1] if len(parts) > 1 else "Customer", phone, current_user.email, address, city, order_no)
        except Exception as exc:
            flash("SkipCash error after order %s: %s" % (order_no, exc), "danger")
            return redirect(url_for("my_orders"))
        pay_url = result.get("payUrl")
        if not pay_url:
            flash("Order %s saved but SkipCash did not return a pay link." % order_no, "danger")
            return redirect(url_for("my_orders"))
        session["skipcash_order"] = order_no
        return redirect(pay_url)

    @app.route("/pay/skipcash/return")
    def pay_skipcash_return():
        order_no = request.args.get("order") or session.get("skipcash_order")
        order = Order.query.filter_by(order_number=order_no).first() if order_no else None
        if order:
            _mark_paid(order)
            flash("Payment received. Receipt for %s." % order.order_number, "success")
            if current_user.is_authenticated and current_user.id == order.user_id:
                return redirect(url_for("order_thanks", order_number=order.order_number))
            return redirect(url_for("track_order", n=order.order_number))
        flash("Payment returned but the order was not found. Check My orders.", "danger")
        return redirect(url_for("my_orders") if current_user.is_authenticated else url_for("track_order"))

    @app.route("/pay/skipcash/webhook", methods=["POST"])
    def pay_skipcash_webhook():
        data = request.get_json(silent=True) or {}
        custom = data.get("Custom1") or (data.get("resultObj") or {}).get("custom1")
        if custom:
            order = Order.query.filter_by(order_number=custom).first()
            if order:
                _mark_paid(order)
        return {"ok": True}, 200
