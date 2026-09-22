from flask import flash, redirect, render_template, request, session, url_for
from flask_login import login_user


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
            return []

    def demo_user(email, name):
        from extensions import db
        from models import User
        from werkzeug.security import generate_password_hash
        import secrets

        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                name=name[:120],
                email=email,
                password_hash=generate_password_hash(secrets.token_urlsafe(16)),
                is_admin=False,
            )
            db.session.add(user)
            db.session.commit()
        login_user(user, remember=True)
        return user

    @app.before_request
    def _safe_pages():
        try:
            path = request.path or "/"
            if path == "/auth/google":
                demo_user("google.demo@1111.local", "Google Demo")
                flash("Signed in with Google (demo).", "success")
                return redirect(url_for("account"))
            if path == "/auth/apple":
                demo_user("apple.demo@1111.local", "Apple Demo")
                flash("Signed in with Apple (demo).", "success")
                return redirect(url_for("account"))
            if request.method == "GET" and path == "/checkout":
                from flask_login import current_user
                from models import CartItem

                has = False
                if getattr(current_user, "is_authenticated", False):
                    has = CartItem.query.filter_by(user_id=current_user.id).first() is not None
                if not has:
                    cart = session.get("cart") or {}
                    has = any(int(v) > 0 for v in cart.values()) if cart else False
                if not has:
                    return render_template("checkout_empty.html")
            if request.method != "GET":
                return None
            if path == "/":
                items = products(16)
                sale = None
                try:
                    from catalog import current_sale, clear_catalog
                    sale = current_sale()
                    clear_catalog()
                except Exception:
                    sale = None
                flash_items = [p for p in items if getattr(p, "is_flash", False)] or items[:8]
                return render_template(
                    "index.html",
                    flash_products=flash_items,
                    live_sale=sale,
                    bestsellers=items[:6],
                    recommended=items,
                    accessory_deals=items,
                    banners=[],
                    promos=[],
                )
            if path in ("/shop", "/shop/product/index"):
                items = products(48)
                q = (request.args.get("q") or "").strip()
                category_id = request.args.get("category") or request.args.get("category_id")
                if q or category_id:
                    from models import Product

                    query = Product.query
                    if category_id:
                        query = query.filter_by(category_id=int(category_id))
                    if q:
                        query = query.filter(Product.name.ilike("%" + q + "%"))
                    items = query.limit(48).all()
                return render_template("shop.html", products=items, q=q)
        except Exception:
            return None
        return None

    @app.route("/become-seller")
    @app.route("/seller")
    def become_seller_alias():
        return redirect("/user/signup-vendor")
