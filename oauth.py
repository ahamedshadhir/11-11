import json
import os
import secrets
import urllib.parse
import urllib.request

from flask import flash, redirect, request, session, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash

GOOGLE_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
APPLE_ID = os.environ.get("APPLE_CLIENT_ID", "")


def _root():
    return (request.host_url or "https://elevenelven.vercel.app/").rstrip("/")


def _user_from_email(email, name):
    from extensions import db
    from models import User

    email = (email or "").strip().lower()
    if not email:
        return None
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    user = User(
        name=(name or email.split("@")[0])[:120],
        email=email,
        password_hash=generate_password_hash(secrets.token_urlsafe(24)),
        is_admin=False,
    )
    db.session.add(user)
    db.session.commit()
    return user


def _demo_login(email, name, label):
    user = _user_from_email(email, name)
    if not user:
        flash(label + " demo login failed.", "danger")
        return redirect(url_for("login"))
    login_user(user)
    flash("Signed in with " + label + " (demo).", "success")
    return redirect(url_for("account"))


def install_oauth(app):
    if getattr(app, "_oauth", False):
        return
    app._oauth = True

    @app.route("/auth/google")
    def auth_google():
        if not GOOGLE_ID or not GOOGLE_SECRET:
            return _demo_login("google.demo@1111.local", "Google Demo", "Google")
        session["oauth_state"] = secrets.token_urlsafe(16)
        params = {
            "client_id": GOOGLE_ID,
            "redirect_uri": _root() + "/auth/google/callback",
            "response_type": "code",
            "scope": "openid email profile",
            "state": session["oauth_state"],
            "prompt": "select_account",
        }
        return redirect("https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params))

    @app.route("/auth/google/callback")
    def auth_google_callback():
        if request.args.get("state") != session.get("oauth_state"):
            return _demo_login("google.demo@1111.local", "Google Demo", "Google")
        code = request.args.get("code")
        if not code:
            return _demo_login("google.demo@1111.local", "Google Demo", "Google")
        body = urllib.parse.urlencode(
            {
                "code": code,
                "client_id": GOOGLE_ID,
                "client_secret": GOOGLE_SECRET,
                "redirect_uri": _root() + "/auth/google/callback",
                "grant_type": "authorization_code",
            }
        ).encode()
        try:
            req = urllib.request.Request(
                "https://oauth2.googleapis.com/token",
                data=body,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                token = json.loads(resp.read().decode())
            ureq = urllib.request.Request(
                "https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": "Bearer " + token.get("access_token", "")},
            )
            with urllib.request.urlopen(ureq, timeout=20) as resp:
                info = json.loads(resp.read().decode())
            user = _user_from_email(info.get("email"), info.get("name"))
            login_user(user)
            return redirect(url_for("account"))
        except Exception:
            return _demo_login("google.demo@1111.local", "Google Demo", "Google")

    @app.route("/auth/apple")
    def auth_apple():
        if not APPLE_ID:
            return _demo_login("apple.demo@1111.local", "Apple Demo", "Apple")
        session["oauth_state"] = secrets.token_urlsafe(16)
        params = {
            "client_id": APPLE_ID,
            "redirect_uri": _root() + "/auth/apple/callback",
            "response_type": "code id_token",
            "response_mode": "form_post",
            "scope": "name email",
            "state": session["oauth_state"],
        }
        return redirect("https://appleid.apple.com/auth/authorize?" + urllib.parse.urlencode(params))

    @app.route("/auth/apple/callback", methods=["GET", "POST"])
    def auth_apple_callback():
        token = request.values.get("id_token") or ""
        email = ""
        name = request.values.get("user")
        try:
            import base64

            payload = token.split(".")[1]
            pad = "=" * (-len(payload) % 4)
            info = json.loads(base64.urlsafe_b64decode(payload + pad))
            email = info.get("email") or ""
        except Exception:
            email = ""
        if name:
            try:
                parsed = json.loads(name).get("name", {})
                name = ((parsed.get("firstName") or "") + " " + (parsed.get("lastName") or "")).strip()
            except Exception:
                name = None
        user = _user_from_email(email, name)
        if not user:
            return _demo_login("apple.demo@1111.local", "Apple Demo", "Apple")
        login_user(user)
        return redirect(url_for("account"))
