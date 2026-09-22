from datetime import datetime
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
