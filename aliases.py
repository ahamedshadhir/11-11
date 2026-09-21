from flask import redirect, render_template, request, session


def install_aliases(app):
    if getattr(app, "_aliases", False):
        return
    app._aliases = True

    @app.context_processor
    def inject_t():
        lang = session.get("lang", "en")

        def t(key):
            try:
                from i18n import translate
                return translate(key, lang)
            except Exception:
                return key

        def arname(name):
            try:
                from i18n import local_name
                return local_name(name, lang)
            except Exception:
                return name

        return {"t": t, "lang": lang, "arname": arname}

    def products(limit=16):
        try:
            from catalog import _load
            return _load()[:limit]
        except Exception:
            try:
                from models import Product
                return Product.query.order_by(Product.id.desc()).limit(limit).all()
            except Exception:
                return []

    @app.before_request
    def _safe_pages():
        try:
            if request.method != "GET":
                return None
            path = request.path or "/"
            if path == "/":
                items = products(16)
                return render_template(
                    "index.html",
                    banners=[],
                    promos=[],
                    flash_products=items[:8],
                    bestsellers=items[:6],
                    recommended=items,
                    accessory_deals=items,
                )
            if path in ("/shop", "/shop/product/index"):
                items = products(48)
                q = (request.args.get("q") or "").strip()
                category_id = request.args.get("category") or request.args.get("category_id")
                if q or category_id:
                    try:
                        from models import Product
                        query = Product.query
                        if category_id:
                            query = query.filter_by(category_id=int(category_id))
                        if q:
                            query = query.filter(Product.name.ilike("%" + q + "%"))
                        items = query.limit(48).all()
                    except Exception:
                        pass
                return render_template("shop.html", products=items, q=q)
        except Exception:
            return None
        return None

    @app.after_request
    def _cache_headers(resp):
        path = request.path or ""
        if path.startswith("/static/"):
            resp.headers["Cache-Control"] = "public, max-age=86400"
        elif request.method == "GET" and path in ("/", "/shop", "/shop/product/index"):
            resp.headers["Cache-Control"] = "public, max-age=30"
        return resp

    @app.route("/become-seller")
    @app.route("/seller")
    def become_seller_alias():
        return redirect("/user/signup-vendor")
