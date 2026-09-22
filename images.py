from urllib.parse import quote
from flask import flash, redirect, url_for
from flask_login import current_user, login_required


def white_url(url):
    url = (url or "").strip()
    if not url:
        return "https://images.weserv.nl/?url=images.unsplash.com/photo-1505740420928-5e560c06d30e&bg=ffffff&fit=contain&w=900&h=900"
    if "weserv.nl" in url and "bg=" in url:
        return url
    raw = url.replace("https://", "").replace("http://", "")
    return "https://images.weserv.nl/?url=" + quote(raw, safe="") + "&bg=ffffff&fit=contain&w=900&h=900&il"


def install_images(app):
    if getattr(app, "_images", False):
        return
    app._images = True

    @app.template_filter("whitebg")
    def whitebg(url):
        return white_url(url)

    @app.route("/admin/products/white-bg", methods=["POST"])
    @login_required
    def admin_white_bg():
        if not getattr(current_user, "is_admin", False):
            return redirect(url_for("login"))
        from extensions import db
        from models import Product

        n = 0
        for p in Product.query.all():
            nxt = white_url(p.image)
            if nxt != p.image:
                p.image = nxt
                n += 1
        db.session.commit()
        flash("White background applied to %s photos." % n, "success")
        return redirect(url_for("admin_products"))
