import os
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

BASE_DIR = Path(__file__).resolve().parent


def _on_vercel():
    return bool(os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))


def _sqlalchemy_url(url: str) -> str:
    if url.startswith("postgres://"):
        url = "postgresql+psycopg2://" + url[len("postgres://"):]
    elif url.startswith("postgresql://") and "+psycopg2" not in url:
        url = "postgresql+psycopg2://" + url[len("postgresql://"):]
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != "channel_binding"]
    if not any(k == "sslmode" for k, _ in query):
        query.append(("sslmode", "require"))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _database_uri():
    url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or os.environ.get("POSTGRES_PRISMA_URL")
    if url:
        return _sqlalchemy_url(url)
    if _on_vercel():
        return "sqlite:////tmp/1111-store.db"
    instance = BASE_DIR / "instance"
    instance.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{instance / 'store.db'}"


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-1111-store-change-me")
    SQLALCHEMY_DATABASE_URI = _database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@1111.local")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
    ITEMS_PER_PAGE = 12
    CURRENCY = "QAR"
    STORE_NAME = "11-11"
    FLASH_SALE_END = "2026-09-30 12:56:00"
