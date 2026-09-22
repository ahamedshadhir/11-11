from flask import redirect, render_template, request, url_for

PHONES = ("iphone", "ipod", "android", "webos", "blackberry", "windows phone")
TABLETS = ("ipad", "tablet", "kindle", "silk", "playbook")


def is_handheld():
    ua = (request.user_agent.string or "").lower()
    if request.args.get("desktop") == "1":
        return False
    if request.args.get("mobile") == "1":
        return True
    return any(tok in ua for tok in PHONES + TABLETS)


def install_mobile(app):
    if getattr(app, "_mobile", False):
        return
    app._mobile = True

    def catalog():
        try:
            from catalog import _load, current_sale, sale_products
            items = _load()
            sale = current_sale()
            return items, sale, sale_products(sale)
        except Exception:
            return [], None, []

    @app.before_request
    def _mobile_gate():
        path = request.path or "/"
        if request.method != "GET":
            return None
        if path.startswith(("/admin", "/api", "/static", "/auth", "/lang")):
            return None
        if path.startswith("/m"):
            return None
        if not is_handheld():
            return None
        if path == "/":
            return redirect("/m")
        if path in ("/shop", "/shop/product/index"):
            return redirect("/m/shop")
        if path == "/cart":
            return redirect("/m/cart")
        if path in ("/login", "/user/login"):
            return redirect("/m/login")
        return None

    @app.route("/m")
    @app.route("/m/")
    def mobile_home():
        items, sale, deals = catalog()
        return render_template("m_index.html", products=(deals or items)[:12], all_products=items[:16], live_sale=sale, flash_products=deals)

    @app.route("/m/shop")
    def mobile_shop():
        items, sale, deals = catalog()
        if request.args.get("flash") and deals:
            items = deals
        return render_template("m_shop.html", products=items[:24], live_sale=sale)

    @app.route("/m/cart")
    def mobile_cart():
        return redirect(url_for("cart"))

    @app.route("/m/login")
    def mobile_login():
        return redirect(url_for("login"))
