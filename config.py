import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _database_uri():
    if os.environ.get("DATABASE_URL"):
        return os.environ["DATABASE_URL"]
    if os.environ.get("VERCEL"):
        return "sqlite:////tmp/1111-store.db"
    return f"sqlite:///{BASE_DIR / 'instance' / 'store.db'}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-1111-store-change-me")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    WTF_CSRF_ENABLED = True
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@1111.local")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
    ITEMS_PER_PAGE = 12
    CURRENCY = "QAR"
    STORE_NAME = "11-11"
    FLASH_SALE_END = "2026-09-30 12:56:00"
