import time
from datetime import datetime
from flask import request, session

_CACHE = {"t": 0, "items": [], "by_cat": {}, "sale": None, "sale_t": 0}


def clear_catalog():
    _CACHE["t"] = 0
    _CACHE["sale_t"] = 0
    _CACHE["items"] = []
    _CACHE["sale"] = None


def _load():
    now = time.time()
    if _CACHE["items"] and now - _CACHE["t"] < 300:
        return _CACHE["items"]
    try:
        from models import Product
        items = Product.query.order_by(Product.id.desc()).limit(24).all()
    except Exception:
        items = _CACHE["items"] or []
    _CACHE["items"] = items
    _CACHE["t"] = now
    groups = {}
    for p in items:
        groups.setdefault(getattr(p, "category_id", None), []).append(p)
    _CACHE["by_cat"] = groups
    return items


def current_sale():
    now = time.time()
    if now - _CACHE["sale_t"] < 60 and _CACHE["sale_t"]:
        return _CACHE["sale"]
    sale = None
    try:
        from flash_sale import FlashSale
        sale = FlashSale.query.filter_by(active=True).order_by(FlashSale.id.desc()).first()
        if sale and sale.ends_at and sale.ends_at < datetime.utcnow():
            sale.active = False
            from extensions import db
            db.session.commit()
            sale = None
    except Exception:
        sale = None
    _CACHE["sale"] = sale
    _CACHE["sale_t"] = now
    return sale


def sale_products(sale):
    if not sale:
        return []
    ids = set(sale.ids())
    if not ids:
        return []
    return [p for p in _load() if p.id in ids]


def suggest_for(pid=None, limit=4):
    items = _load()
    return [p for p in items if p.id != pid][:limit]


def install_catalog(app):
    if getattr(app, "_catalog", False):
        return
    app._catalog = True

    @app.template_filter("arname")
    def arname(name):
        try:
            from i18n import local_name
            return local_name(name, session.get("lang", "en"))
        except Exception:
            return name or ""

    @app.context_processor
    def inject_catalog():
        items = _load()
        sale = current_sale()
        return {
            "all_products": items[:16],
            "flash_products": sale_products(sale),
            "ai_picks": [],
            "live_sale": sale,
        }

    @app.after_request
    def _cache_ok(resp):
        if request.method == "GET" and resp.status_code == 200 and request.path.startswith("/static/"):
            resp.headers["Cache-Control"] = "public, max-age=86400"
        return resp

    @app.route("/api/suggest")
    def api_suggest():
        pid = request.args.get("pid", type=int)
        data = [{"id": p.id, "name": p.name, "price": p.price, "image": p.image, "slug": p.slug} for p in suggest_for(pid, 6)]
        return {"items": data}
