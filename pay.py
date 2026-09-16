from flask import redirect, request, url_for
from flask_login import current_user, login_required


def install_pay(app):
    if getattr(app, "_pay_router", False):
        return
    app._pay_router = True

    @app.route("/checkout/pay", methods=["POST"])
    @login_required
    def checkout_pay():
        method = (request.form.get("payment_method") or "cod").lower()
        if method == "skipcash":
            return app.view_functions["pay_skipcash"]()
        if method == "sadad":
            return app.view_functions["pay_sadad"]()
        return app.view_functions["checkout"]()
