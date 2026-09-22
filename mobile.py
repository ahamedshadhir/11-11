from flask import redirect, render_template, request, session, url_for
from flask_login import current_user

PHONES = ("iphone", "ipod", "android", "webos", "blackberry", "windows phone")
TABLETS = ("ipad", "tablet", "kindle", "silk", "playbook")


def is_handheld():
    ua = (request.user_agent.string or "").lower()
    if request.args.get("desktop") == "1" or session.get("force_desktop"):
        if request.args.get("desktop") == "1":
            session["force_desktop"] = True
        return False
    if request.args.get("mobile") == "1":
        session.pop("force_desktop", None)
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

    def cart_rows():
        rows = []
        try:
            from models import CartItem, Product
            if getattr(current_user, "is_authenticated", False):
                for it in CartItem.query.filter_by(user_id=current_user.id).all():
                    if it.product:
                        rows.append({"product": it.product, "qty": it.quantity, "line": it.product.price * it.quantity})
            else:
                guest = session.get("cart") or {}
                ids = [int(k) for k in guest.keys() if str(k).isdigit()]
                if ids:
                    found = {p.id: p for p in Product.query.filter(Product.id.in_(ids)).all()}
                    for pid, qty in guest.items():
                        p = found.get(int(pid))
                        if p:
                            rows.append({"product": p, "qty": int(qty), "line": p.price * int(qty)})
        except Exception:
            rows = []
        return rows

    @app.before_request
    def _mobile_gate():
        path = request.path or "/"
        if request.method != "GET":
            return None
        if path.startswith(("/admin", "/api", "/static", "/auth", "/lang", "/m")):
            return None
        if not is_handheld():
            return None
        mapping = {
            "/": "/m",
            "/shop": "/m/shop",
            "/shop/product/index": "/m/shop",
            "/cart": "/m/cart",
            "/wishlist": "/m/wishlist",
            "/login": "/m/login",
            "/user/login": "/m/login",
            "/register": "/m/register",
            "/account": "/m/account",
            "/checkout": "/m/checkout",
        }
        if path in mapping:
            qs = request.query_string.decode() if request.query_string else ""
            return redirect(mapping[path] + (("?" + qs) if qs else ""))
        return None

    @app.route("/m")
    @app.route("/m/")
    def mobile_home():
        items, sale, deals = catalog()
        return render_template("m_index.html", products=items[:12], live_sale=sale, flash_products=deals)

    @app.route("/m/shop")
    def mobile_shop():
        items, sale, deals = catalog()
        q = (request.args.get("q") or "").strip()
        if request.args.get("flash") and deals:
            items = deals
        elif q:
            items = [p for p in items if q.lower() in (p.name or "").lower()]
        return render_template("m_shop.html", products=items[:24], live_sale=sale, q=q)

    @app.route("/m/product/<int:pid>/<slug>")
    def mobile_product(pid, slug):
        from models import Product
        p = Product.query.get_or_404(pid)
        items, sale, _ = catalog()
        related = [x for x in items if x.id != p.id][:4]
        return render_template("m_product.html", product=p, related=related, live_sale=sale)

    @app.route("/m/cart")
    def mobile_cart():
        rows = cart_rows()
        total = sum(r["line"] for r in rows)
        return render_template("m_cart.html", rows=rows, total=total)

    @app.route("/m/wishlist")
    def mobile_wishlist():
        return render_template("m_shop.html", products=[], q="", heading="Wishlist")

    @app.route("/m/login", methods=["GET", "POST"])
    def mobile_login():
        if request.method == "POST":
            return redirect("/login", code=307)
        return render_template("m_login.html")

    @app.route("/m/register")
    def mobile_register():
        return redirect(url_for("register"))

    @app.route("/m/account")
    def mobile_account():
        if not getattr(current_user, "is_authenticated", False):
            return redirect("/m/login")
        return render_template("m_account.html")

    @app.route("/m/checkout")
    def mobile_checkout():
        rows = cart_rows()
        if not rows:
            return render_template("m_cart.html", rows=[], total=0)
        return redirect("/checkout")
