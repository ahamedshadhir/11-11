import base64
import hashlib
import json
import os
import secrets
import string
from datetime import datetime
from urllib.parse import quote
from urllib.request import Request, urlopen

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

API = os.environ.get("SADAD_API", "https://api.sadadqatar.com/api-v4")
MERCHANT_ID = os.environ.get("SADAD_MERCHANT_ID", os.environ.get("SADAD_ID", ""))
SECRET = os.environ.get("SADAD_SECRET", os.environ.get("SADAD_SECRET_KEY", ""))
DOMAIN = os.environ.get("SADAD_DOMAIN", "elevenelven.vercel.app")
CHECKOUT_URL = os.environ.get("SADAD_CHECKOUT_URL", "https://sadadqa.com/webpurchase")
IV = b"@@@@&&&&####$$$$"


def _aes_encrypt(text, key_str):
    key = (key_str.encode("utf-8") + b"\0" * 16)[:16]
    padder = padding.PKCS7(128).padder()
    data = padder.update(text.encode("utf-8")) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(IV))
    enc = cipher.encryptor()
    raw = enc.update(data) + enc.finalize()
    return base64.b64encode(raw).decode()


def local_checksum(post_data):
    """SADAD PHP getChecksumFromString: json({postData, secretKey}) + |salt, SHA256, AES-128-CBC."""
    payload = {"postData": post_data, "secretKey": SECRET}
    raw = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    salt = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(4))
    hashed = hashlib.sha256((raw + "|" + salt).encode("utf-8")).hexdigest() + salt
    key = quote(SECRET, safe="") + str(MERCHANT_ID)
    return _aes_encrypt(hashed, key)


def api_checksum(fields):
    payload = {
        "merchant_id": MERCHANT_ID,
        "WEBSITE": DOMAIN,
        "TXN_AMOUNT": fields["TXN_AMOUNT"],
        "ORDER_ID": fields["ORDER_ID"],
        "CALLBACK_URL": fields["CALLBACK_URL"],
        "MOBILE_NO": fields["MOBILE_NO"],
        "EMAIL": fields["EMAIL"],
        "productdetail": [
            {
                "order_id": fields["ORDER_ID"],
                "quantity": "1",
                "amount": fields["TXN_AMOUNT"],
            }
        ],
        "txnDate": fields["txnDate"],
        "VERSION": "2.1",
    }
    req = Request(
        API + "/userbusinesses/generateChecksum",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "secretkey": SECRET,
            "Origin": "https://" + DOMAIN,
        },
        method="POST",
    )
    with urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    return data.get("checksum") or data.get("checksumhash")


def install_sadad(app):
    if getattr(app, "_sadad", False):
        return
    app._sadad = True
    from extensions import db
    from models import CartItem, Order, OrderItem

    @app.route("/pay/sadad", methods=["POST"])
    @login_required
    def pay_sadad():
        items = CartItem.query.filter_by(user_id=current_user.id).all()
        rows = [(it.product, it.quantity) for it in items if it.product]
        if not rows:
            flash("Your cart is empty.", "danger")
            return redirect(url_for("cart"))
        subtotal = sum(p.price * q for p, q in rows)
        shipping = 0 if subtotal >= 200 else 25
        discount = round(subtotal * 0.10, 2) if session.get("coupon") == "FLASH10" else 0
        total = max(0, subtotal + shipping - discount)
        order_no = "1111-" + secrets.token_hex(4).upper()
        name = request.form.get("name") or current_user.name
        phone = "".join(ch for ch in (request.form.get("phone") or current_user.phone or "50000000") if ch.isdigit())[-10:]
        email = current_user.email or request.form.get("email") or "buyer@1111.local"
        order = Order(
            user_id=current_user.id,
            order_number=order_no,
            status="pending",
            payment_method="sadad",
            subtotal=subtotal,
            shipping=shipping,
            total=total,
            shipping_name=name,
            shipping_phone=phone,
            shipping_address=request.form.get("address") or "Doha",
            shipping_city=request.form.get("city") or "Doha",
        )
        db.session.add(order)
        db.session.flush()
        for p, q in rows:
            db.session.add(
                OrderItem(order_id=order.id, product_id=p.id, name=p.name, price=p.price, quantity=q, image=p.image)
            )
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        callback = request.url_root.rstrip("/") + "/pay/sadad/return"
        if not MERCHANT_ID or not SECRET:
            return render_template("sadad_setup.html", order=order, domain=DOMAIN)
        fields = {
            "merchant_id": str(MERCHANT_ID),
            "ORDER_ID": order_no,
            "WEBSITE": DOMAIN,
            "TXN_AMOUNT": f"{total:.2f}",
            "CUST_ID": email,
            "EMAIL": email,
            "MOBILE_NO": phone or "50000000",
            "CALLBACK_URL": callback,
            "txnDate": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "SADAD_WEBCHECKOUT_PAGE_LANGUAGE": "ENG",
        }
        try:
            checksum = api_checksum(fields)
        except Exception:
            checksum = local_checksum(fields)
        return render_template(
            "sadad_redirect.html",
            action=CHECKOUT_URL,
            fields=fields,
            checksum=checksum,
            item_name=rows[0][0].name if rows else "11-11 order",
            item_qty=sum(q for _, q in rows),
            amount=f"{total:.2f}",
            order_id=order_no,
        )

    @app.route("/pay/sadad/return", methods=["GET", "POST"])
    def pay_sadad_return():
        order_no = request.values.get("ORDERID") or request.values.get("ORDER_ID") or request.values.get("order")
        status = (request.values.get("STATUS") or request.values.get("RESPMSG") or "").upper()
        order = Order.query.filter_by(order_number=order_no).first() if order_no else None
        if order and ("SUCCESS" in status or status in {"1", "3", "TXN_SUCCESS"}):
            order.status = "paid"
            db.session.commit()
        if order:
            return redirect(url_for("order_thanks", order_number=order.order_number))
        flash("Sadad callback received.", "info")
        return redirect(url_for("my_orders") if current_user.is_authenticated else url_for("index"))
