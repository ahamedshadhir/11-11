from urllib.parse import quote
from flask import flash, redirect, url_for
from flask_login import current_user, login_required


def _pass(url):
    u = (url or "").strip()
    if not u:
        return "https://cdn.dummyjson.com/product-images/smartphones/iphone-13-pro/thumbnail.webp"
    return u


def img_card(url):
    u = _pass(url)
    if "dummyjson.com" in u:
        return u.replace("/1.webp", "/thumbnail.webp")
    if "weserv.nl" in u:
        return u
    raw = u.replace("https://", "").replace("http://", "")
    return "https://images.weserv.nl/?url=" + quote(raw, safe="") + "&w=400&h=400&fit=contain&bg=ffffff&output=webp&q=75"


def img_hero(url):
    u = _pass(url)
    if "dummyjson.com" in u:
        return u.replace("/thumbnail.webp", "/1.webp")
    if "weserv.nl" in u:
        return u
    raw = u.replace("https://", "").replace("http://", "")
    return "https://images.weserv.nl/?url=" + quote(raw, safe="") + "&w=900&h=900&fit=contain&bg=ffffff&output=webp&q=80"


def white_url(url):
    return img_card(url)


def install_images(app):
    if getattr(app, "_images", False):
        return
    app._images = True

    @app.template_filter("whitebg")
    def whitebg(url):
        return img_card(url)

    @app.template_filter("imgcard")
    def imgcard(url):
        return img_card(url)

    @app.template_filter("imghero")
    def imghero(url):
        return img_hero(url)

    @app.route("/admin/products/white-bg", methods=["POST"])
    @login_required
    def admin_white_bg():
        if not getattr(current_user, "is_admin", False):
            return redirect(url_for("login"))
        flash("Photos already use optimized packshots.", "success")
        return redirect(url_for("admin_products"))
