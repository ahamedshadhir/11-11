from urllib.parse import quote
from flask import flash, redirect, url_for
from flask_login import current_user, login_required


def white_url(url):
    url = (url or "").strip()
    if not url:
        return "https://images.unsplash.com/photo-1510557880182-3d4d3cba35a5?auto=format&fit=crop&w=900&q=80"
    if "weserv.nl" in url:
        return url
    raw = url.replace("https://", "").replace("http://", "")
    return "https://images.weserv.nl/?url=" + quote(raw, safe="") + "&bg=ffffff&fit=contain&w=900&h=900"


def install_images(app):
    if getattr(app, "_images", False):
        return
    app._images = True

    @app.template_filter("whitebg")
    def whitebg(url):
        try:
            return white_url(url)
        except Exception:
            return url or ""

    @app.route("/admin/products/white-bg", methods=["POST"])
    @login_required
    def admin_white_bg():
        if not getattr(current_user, "is_admin", False):
            return redirect(url_for("login"))
        from extensions import db
        from models import Product
        n = 0
        try:
            for p in Product.query.all():
                nxt = white_url(p.image)
                if nxt != p.image:
                    p.image = nxt
                    n += 1
            db.session.commit()
        except Exception:
            pass
        flash("White background applied to %s photos." % n, "success")
        return redirect(url_for("admin_products"))
