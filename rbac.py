from functools import wraps

from flask import abort, flash, redirect, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import text

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
    user.is_admin = role in ("staff", "admin")
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

    @app.before_request
    def _rbac_guard():
        path = request.path or ""
        if not path.startswith("/admin"):
            return None
        if path.startswith("/admin/products/white-bg"):
            allowed = ("staff", "admin")
        elif path.startswith("/admin/users") or path.startswith("/admin/settings"):
            allowed = ("admin",)
        else:
            allowed = ("staff", "admin")
        if not getattr(current_user, "is_authenticated", False):
            return None
        if not has_role(current_user, *allowed):
            abort(403)
        return None
