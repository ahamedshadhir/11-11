import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask, redirect, request
from flask_login import current_user, login_user

from config import Config
from extensions import db, login_manager
from models import User

app = Flask(__name__, template_folder=str(ROOT / "templates"), static_folder=str(ROOT / "static"))
app.config.from_object(Config)
app.secret_key = os.environ.get("SECRET_KEY") or app.config.get("SECRET_KEY") or "dev-1111-store-change-me"
app.config["SECRET_KEY"] = app.secret_key
db.init_app(app)
login_manager.init_app(app)

FORM = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Login | 11-11</title>
<style>
body{margin:0;font-family:Arial,sans-serif;background:#f6f3ee;color:#420e15}
.wrap{max-width:420px;margin:8vh auto;padding:28px;background:#fff;border:1px solid #e7dcc8}
h2{margin:0 0 8px}
.muted{color:#7a5a3a;font-size:14px}
label{display:block;margin:12px 0 4px;font-size:13px}
input{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #d9c7a8}
button{margin-top:16px;width:100%;padding:12px;border:0;background:#420e15;color:#fff;font-weight:700;cursor:pointer}
.err{background:#fb2c36;color:#fff;padding:8px 10px;margin:12px 0}
.ok{background:#2e7d32;color:#fff;padding:8px 10px;margin:12px 0}
a{color:#be923b}
</style></head>
<body><div class="wrap">
<h2>Login</h2>
<p class="muted">Demo: demo@1111.local / demo123<br>Admin: admin@1111.local / admin123</p>
%s
<form method="post" action="/login">
<label>Email</label><input type="email" name="email" required>
<label>Password</label><input type="password" name="password" required>
<button type="submit">Sign in</button>
</form>
<p class="muted" style="margin-top:16px"><a href="/">Back to store</a></p>
</div></body></html>"""


def page(msg=""):
    return FORM % (msg or "")


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
@app.route("/user/login", methods=["GET", "POST"])
def login():
    if getattr(current_user, "is_authenticated", False) and request.method == "GET":
        return redirect("/")
    if request.method != "POST":
        return page()
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
        ok = user is not None and allowed
        if user is not None and not ok:
            try:
                ok = bool(user.check_password(password))
            except Exception:
                ok = False
        if not ok or user is None:
            return page('<div class="err">Invalid email or password.</div>')
        login_user(user, remember=False)
        return redirect("/")
    except Exception as exc:
        try:
            db.session.rollback()
        except Exception:
            pass
        return page('<div class="err">%s</div>' % exc)
