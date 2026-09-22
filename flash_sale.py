from datetime import datetime, timedelta
from extensions import db


class FlashSale(db.Model):
    __tablename__ = "flash_sale"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), default="Flash sale")
    discount = db.Column(db.Float, default=10)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=False)
    product_ids = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def ids(self):
        out = []
        for part in (self.product_ids or "").split(","):
            part = part.strip()
            if part.isdigit():
                out.append(int(part))
        return out


def apply_sale(sale, on):
    from models import Product
    from catalog import clear_catalog

    Product.query.update({Product.is_flash: False})
    ids = sale.ids()
    if on:
        if not ids:
            sale.active = False
            db.session.commit()
            clear_catalog()
            return False
        Product.query.filter(Product.id.in_(ids)).update({Product.is_flash: True}, synchronize_session=False)
        sale.active = True
        sale.starts_at = sale.starts_at or datetime.utcnow()
        sale.ends_at = sale.ends_at or (datetime.utcnow() + timedelta(hours=24))
    else:
        sale.active = False
    db.session.commit()
    clear_catalog()
    return True
