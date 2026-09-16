import json
import os
import secrets
from urllib.request import Request, urlopen

from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

API = os.environ.get("SADAD_API", "https://api.sadadqatar.com/api-v4")
MERCHANT_ID = os.environ.get("SADAD_MERCHANT_ID", "")
SECRET = os.environ.get("SADAD_SECRET", "")
DOMAIN = os.environ.get("SADAD_DOMAIN", "elevenelven.vercel.app")
CHECKOUT_URL = os.environ.get("SADAD_CHECKOUT_URL", "https://sadadqa.com/webpurchase")


def generate_checksum(order_id, amount, email, mobile, callback):
    payload = {
        "merchant_id": MERCHANT_ID,
        "WEBSITE": DOMAIN,
        "TXN_AMOUNT": f"{float(amount):.2f}",
        "ORDER_ID": order_id,
        "CALLBACK_URL": callback,
        "MOBILE_NO": mobile,
        "EMAIL": email,
        "productdetail": [{"order_id": order_id, "quantity": "1", "amount": f"{float(amount):.2f}"}],
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
        phone = request.form.get("phone") or current_user.phone or "50000000"
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
            db.session.add(OrderItem(order_id=order.id, product_id=p.id, name=p.name, price=p.price, quantity=q, image=p.image))
        CartItem.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        callback = request.url_root.rstrip("/") + "/pay/sadad/return"
        if not MERCHANT_ID or not SECRET:
            return render_template("sadad_sandbox.html", order=order)
        try:
            checksum = generate_checksum(order_no, total, current_user.email, phone, callback)
        except Exception as exc:
            flash("Sadad checksum failed, using sandbox page: %s" % exc, "info")
            return render_template("sadad_sandbox.html", order=order)
        return render_template(
            "sadad_redirect.html",
            action=CHECKOUT_URL,
            merchant_id=MERCHANT_ID,
            order_id=order_no,
            amount=f"{total:.2f}",
            checksum=checksum,
            callback=callback,
            email=current_user.email,
            mobile=phone,
        )

    @app.route("/pay/sadad/sandbox", methods=["POST"])
    @login_required
    def pay_sadad_sandbox():
        order_no = request.form.get("order")
        order = Order.query.filter_by(order_number=order_no, user_id=current_user.id).first_or_404()
        if request.form.get("result") == "success":
            order.status = "paid"
            db.session.commit()
            flash("Sadad sandbox payment successful.", "success")
        else:
            order.status = "cancelled"
            db.session.commit()
            flash("Sadad sandbox payment cancelled.", "info")
        return redirect(url_for("order_thanks", order_number=order.order_number))

    @app.route("/pay/sadad/return", methods=["GET", "POST"])
    def pay_sadad_return():
        order_no = request.values.get("ORDERID") or request.values.get("ORDER_ID") or request.values.get("order")
        status = (request.values.get("STATUS") or "").upper()
        order = Order.query.filter_by(order_number=order_no).first() if order_no else None
        if order and ("SUCCESS" in status or status in {"1", "3", "TXN_SUCCESS"}):
            order.status = "paid"
            db.session.commit()
            return redirect(url_for("order_thanks", order_number=order.order_number))
        if order:
            return redirect(url_for("order_thanks", order_number=order.order_number))
        return redirect(url_for("my_orders") if current_user.is_authenticated else url_for("index"))
