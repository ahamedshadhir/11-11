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
    try:
        from models import Product
        items = Product.query.order_by(Product.id.desc()).limit(50).all()
    except Exception:
        items = _CACHE["items"] or []
    _CACHE["items"] = items
    _CACHE["t"] = time.time()
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
    return [p for p in _load() if p.id in ids]


def install_catalog(app):
    if getattr(app, "_catalog", False):
        return
    app._catalog = True

    @app.template_filter("arname")
    def arname(name):
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
