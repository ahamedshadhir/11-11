from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user


def install_aliases(app):
    if getattr(app, "_aliases", False):
        return
    app._aliases = True

    @app.route("/become-seller")
    @app.route("/seller")
    def become_seller_alias():
        return redirect("/user/signup-vendor")

    @app.route("/checkout/empty")
    def checkout_empty():
        return render_template("checkout_empty.html")

    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("500.html"), 500
