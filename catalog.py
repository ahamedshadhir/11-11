import time

_CACHE = {"t": 0, "items": []}

def install_catalog(app):
    if getattr(app, "_catalog", False):
        return
    app._catalog = True

    @app.context_processor
    def inject_catalog():
        now = time.time()
        if _CACHE["items"] and now - _CACHE["t"] < 180:
            return {"all_products": _CACHE["items"]}
        try:
            from models import Product
            items = Product.query.order_by(Product.id.desc()).limit(24).all()
        except Exception:
            items = []
        _CACHE["items"] = items
        _CACHE["t"] = now
        return {"all_products": items}
