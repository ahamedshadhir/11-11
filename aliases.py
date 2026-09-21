from flask import redirect, render_template, request, session


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

    def _products(limit=16):
        try:
            from models import Product
            return Product.query.order_by(Product.id.desc()).limit(limit).all()
        except Exception:
            return []

    @app.before_request
    def _safe_pages():
        path = request.path or "/"
        if request.method != "GET":
            return None
        if path == "/":
            products = _products(16)
            return render_template(
                "index.html",
                banners=[],
                promos=[],
                flash_products=products[:8],
                bestsellers=products[:6],
                recommended=products,
                accessory_deals=products,
            )
        if path in ("/shop", "/shop/product/index"):
            products = _products(48)
            try:
                from models import Product
                q = (request.args.get("q") or "").strip()
                category_id = request.args.get("category") or request.args.get("category_id")
                query = Product.query
                if category_id:
                    query = query.filter_by(category_id=int(category_id))
                if q:
                    query = query.filter(Product.name.ilike("%" + q + "%"))
                products = query.limit(48).all()
            except Exception:
                pass
            return render_template("shop.html", products=products, q=request.args.get("q", ""))
        return None

    @app.route("/become-seller")
    @app.route("/seller")
    def become_seller_alias():
        return redirect("/user/signup-vendor")
