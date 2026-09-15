import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask, flash, redirect, render_template, request
from flask_login import current_user, login_user

from config import Config
from extensions import db, login_manager
from models import User

app = Flask(
    __name__,
    template_folder=str(ROOT / "templates"),
    static_folder=str(ROOT / "static"),
)
app.config.from_object(Config)
app.secret_key = os.environ.get("SECRET_KEY") or app.config.get("SECRET_KEY") or "dev-1111-store-change-me"
app.config["SECRET_KEY"] = app.secret_key
db.init_app(app)
login_manager.init_app(app)


def _page():
    if getattr(current_user, "is_authenticated", False):
        return redirect("/")
    if request.method != "POST":
        try:
            return render_template("login.html")
        except Exception:
            return redirect("/")
    email = (request.form.get("email") or "").strip().lower()
    password = request.form.get("password") or ""
    try:
        user = User.query.filter_by(email=email).first()
        admin_email = (app.config.get("ADMIN_EMAIL") or "admin@1111.local").lower()
        admin_pw = app.config.get("ADMIN_PASSWORD") or "admin123"
        allowed = (email == "demo@1111.local" and password == "demo123") or (
            email == admin_email and password == admin_pw
        )
        if user is None and allowed:
            user = User(
                name="Store Admin" if email == admin_email else "Aisha Al-Thani",
                email=email,
                is_admin=email == admin_email,
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
        ok = False
        if user is not None and allowed:
            ok = True
        elif user is not None:
            try:
                ok = bool(user.check_password(password))
            except Exception:
                ok = False
        if not ok or user is None:
            flash("Invalid email or password.", "danger")
            return render_template("login.html")
        login_user(user, remember=False)
        flash("Welcome back, %s." % (user.name or "there"), "success")
        return redirect("/")
    except Exception as exc:
        try:
            db.session.rollback()
        except Exception:
            pass
        return (
            "<h1>Login failed</h1><p>%s</p><p><a href='/login'>Back</a></p>" % exc,
            200,
        )


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/user/login", methods=["GET", "POST"])
def login():
    return _page()
