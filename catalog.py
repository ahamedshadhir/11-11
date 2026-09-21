import time
from flask import request, session

_CACHE = {"t": 0, "items": [], "by_cat": {}}


def _load():
    now = time.time()
    if _CACHE["items"] and now - _CACHE["t"] < 600:
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
        groups.setdefault(p.category_id, []).append(p)
    _CACHE["by_cat"] = groups
    return items


def suggest_for(pid=None, limit=4):
    items = _load()
    if not items:
        return []
    current = next((p for p in items if p.id == pid), None)
    pool = list(_CACHE["by_cat"].get(getattr(current, "category_id", None), items))
    out = [p for p in pool if p.id != pid][:limit]
    if len(out) < limit:
        extra = [p for p in items if p.id != pid and p not in out]
        out.extend(extra[: limit - len(out)])
    return out


def install_catalog(app):
    if getattr(app, "_catalog", False):
        return
    app._catalog = True

    @app.context_processor
    def inject_catalog():
        items = _load()
        last = session.get("last_pid")
        return {
            "all_products": items[:24],
            "ai_picks": suggest_for(last, 4),
        }

    @app.before_request
    def remember_product():
        pid = (request.view_args or {}).get("pid")
        if pid:
            session["last_pid"] = pid

    @app.route("/api/suggest")
    def api_suggest():
        pid = request.args.get("pid", type=int)
        data = []
        for p in suggest_for(pid, 6):
            data.append({"id": p.id, "name": p.name, "price": p.price, "image": p.image, "slug": p.slug})
        return {"items": data}

    @app.after_request
    def static_speed(resp):
        path = request.path or ""
        if path.startswith("/static/"):
            resp.headers["Cache-Control"] = "public, max-age=86400, immutable"
        elif request.method == "GET" and path in ("/", "/shop", "/shop/product/index"):
            resp.headers["Cache-Control"] = "public, max-age=60"
        return resp
