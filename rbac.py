from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import text

ROLES = ("customer", "vendor", "staff", "admin")
LEVEL = {"customer": 0, "vendor": 1, "staff": 2, "admin": 3}


def role_of(user):
    if not user or not getattr(user, "is_authenticated", False):
        return "guest"
    stored = (getattr(user, "role", None) or "").strip().lower()
    if stored in LEVEL:
        return stored
    if getattr(user, "is_admin", False):
        return "admin"
    if getattr(user, "is_vendor", False):
        return "vendor"
    return "customer"


def has_role(user, *allowed):
    if not allowed:
        return True
    current = role_of(user)
    if current == "admin":
        return True
    return current in allowed


def set_role(user, role):
    role = (role or "customer").strip().lower()
    if role not in LEVEL:
        role = "customer"
    try:
        user.role = role
    except Exception:
        pass
    user.is_admin = role == "admin"
    user.is_vendor = role in ("vendor", "admin")
    return role


def roles_required(*allowed):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapped(*args, **kwargs):
            if not has_role(current_user, *allowed):
                abort(403)
            return fn(*args, **kwargs)

        return wrapped

    return decorator


def install_rbac(app):
    if getattr(app, "_rbac", False):
        return
    app._rbac = True
    from extensions import db

    with app.app_context():
        for stmt in (
            'ALTER TABLE "user" ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT \'customer\'',
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'customer'",
        ):
            try:
                db.session.execute(text(stmt))
                db.session.commit()
            except Exception:
                db.session.rollback()

    @app.context_processor
    def inject_rbac():
        current = role_of(current_user) if getattr(current_user, "is_authenticated", False) else "guest"
        return {"user_role": current, "is_staff": current in ("staff", "admin"), "is_admin_user": current == "admin"}

    @app.errorhandler(403)
    def forbidden(_e):
        flash("You do not have access to that page.", "danger")
        if getattr(current_user, "is_authenticated", False):
            return redirect(url_for("account")), 403
        return redirect(url_for("login")), 403
