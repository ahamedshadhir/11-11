import time
from datetime import datetime
from flask import request, session

_CACHE = {"t": 0, "items": [], "by_cat": {}}


def clear_catalog():
    _CACHE["t"] = 0
    _CACHE["items"] = []
    _CACHE["by_cat"] = {}


def _load():
    now = time.time()
    if _CACHE["items"] and now - _CACHE["t"] < 30:
        return _CACHE["items"]
    try:
        from models import Product
        items = Product.query.order_by(Product.id.desc()).limit(48).all()
    except Exception:
        items = []
    _CACHE["items"] = items
    _CACHE["t"] = now
    groups = {}
    for p in items:
        groups.setdefault(getattr(p, "category_id", None), []).append(p)
    _CACHE["by_cat"] = groups
    return items


def current_sale():
    try:
        from flash_sale import FlashSale
        sale = FlashSale.query.filter_by(active=True).order_by(FlashSale.id.desc()).first()
        if not sale:
            return None
        if sale.ends_at and sale.ends_at < datetime.utcnow():
            sale.active = False
            from extensions import db
            from models import Product
            Product.query.update({Product.is_flash: False})
            db.session.commit()
            clear_catalog()
            return None
        return sale
    except Exception:
        return None


def sale_products(sale):
    if not sale:
        return []
    ids = sale.ids()
    if not ids:
        return []
    try:
        from models import Product
        rows = Product.query.filter(Product.id.in_(ids)).all()
        order = {i: n for n, i in enumerate(ids)}
        rows.sort(key=lambda p: order.get(p.id, 999))
        return rows
    except Exception:
        return []


def suggest_for(pid=None, limit=4):
    items = _load()
    if not items:
        return []
    current = next((p for p in items if p.id == pid), None)
    cat = getattr(current, "category_id", None) if current else None
    pool = list(_CACHE["by_cat"].get(cat, items))
    out = [p for p in pool if p.id != pid][:limit]
    if len(out) < limit:
        extra = [p for p in items if p.id != pid and p not in out]
        out.extend(extra[: limit - len(out)])
    return out


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
            "all_products": items[:24],
            "flash_products": sale_products(sale),
            "ai_picks": suggest_for(session.get("last_pid"), 4),
            "live_sale": sale,
        }

    @app.route("/api/suggest")
    def api_suggest():
        pid = request.args.get("pid", type=int)
        data = [{"id": p.id, "name": p.name, "price": p.price, "image": p.image, "slug": p.slug} for p in suggest_for(pid, 6)]
        return {"items": data}
