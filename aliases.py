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
            from i18n import translate
            def t(key):
                return translate(key, lang)
        except Exception:
            def t(key):
                return key
        return {"t": t, "lang": lang}

    @app.route("/become-seller")
    @app.route("/seller")
    def become_seller_alias():
        return redirect("/user/signup-vendor")

    @app.before_request
    def _checkout_empty_guard():
        if request.method != "GET":
            return None
        if request.path not in ("/checkout", "/shop/cart/checkout"):
            return None
        try:
            from models import CartItem
            has = False
            if getattr(current_user, "is_authenticated", False):
                has = CartItem.query.filter_by(user_id=current_user.id).first() is not None
            if not has:
                cart = session.get("cart") or {}
                has = any(int(v) > 0 for v in cart.values()) if cart else False
            if not has:
                return render_template("checkout_empty.html")
        except Exception:
            return None

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("500.html"), 500
