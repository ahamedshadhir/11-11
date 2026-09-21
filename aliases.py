from flask import redirect, render_template, request, session
from flask_login import current_user


def install_aliases(app):
    if getattr(app, "_aliases", False):
        return
    app._aliases = True

    @app.context_processor
    def inject_t():
        lang = session.get("lang", "en")
        try:
            from i18n import translate, local_name

            def t(key):
                return translate(key, lang)

            def arname(name):
                return local_name(name, lang)
        except Exception:

            def t(key):
                return key

            def arname(name):
                return name

        return {"t": t, "lang": lang, "arname": arname}

    @app.template_filter("arname")
    def arname_filter(name):
        try:
            from i18n import local_name
            return local_name(name, session.get("lang", "en"))
        except Exception:
            return name or ""

    def safe_home():
        products = []
        try:
            from models import Product
            products = Product.query.order_by(Product.id.desc()).limit(16).all()
        except Exception:
            products = []
        return render_template(
            "index.html",
            banners=[],
            promos=[],
            flash_products=products[:8],
            bestsellers=products[:6],
            recommended=products,
            accessory_deals=products,
        )

    def safe_shop():
        products = []
        try:
            from models import Product
            query = Product.query
            q = (request.args.get("q") or "").strip()
            category_id = request.args.get("category") or request.args.get("category_id")
            if category_id:
                query = query.filter_by(category_id=int(category_id))
            if q:
                query = query.filter(Product.name.ilike("%" + q + "%"))
            products = query.limit(48).all()
        except Exception:
            products = []
        return render_template("shop.html", products=products, q=request.args.get("q", ""))

    def safe_product(pid, slug="item"):
        from models import Product, Review

        product = Product.query.get_or_404(pid)
        related = []
        reviews = []
        try:
            related = (
                Product.query.filter(Product.category_id == product.category_id, Product.id != pid)
                .limit(4)
                .all()
            )
        except Exception:
            pass
        try:
            reviews = Review.query.filter_by(product_id=pid).all()
        except Exception:
            pass
        return render_template("product.html", product=product, related=related, reviews=reviews)

    app.view_functions["index"] = safe_home
    app.view_functions["shop"] = safe_shop
    if "product_detail" in app.view_functions:
        app.view_functions["product_detail"] = safe_product

    @app.route("/become-seller")
    @app.route("/seller")
    def become_seller_alias():
        return redirect("/user/signup-vendor")

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404
