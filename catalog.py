from flask import session

def install_catalog(app):
    if getattr(app, '_catalog', False):
        return
    app._catalog = True

    @app.context_processor
    def inject_catalog():
        try:
            from models import Product
            items = Product.query.order_by(Product.id.desc()).limit(36).all()
        except Exception:
            items = []
        return {'all_products': items}
