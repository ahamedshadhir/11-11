from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(40))
    is_admin = db.Column(db.Boolean, default=False)
    is_vendor = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship("CartItem", backref="user", cascade="all, delete-orphan")
    wishlist_items = db.relationship("WishlistItem", backref="user", cascade="all, delete-orphan")
    orders = db.relationship("Order", backref="user", cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="user", cascade="all, delete-orphan")
    addresses = db.relationship("Address", backref="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password: str) -> bool:
        try:
            return bool(self.password_hash) and check_password_hash(self.password_hash, password)
        except Exception:
            return False


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    label = db.Column(db.String(80), default="Home")
    line1 = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), default="Qatar")
    phone = db.Column(db.String(40))
    is_default = db.Column(db.Boolean, default=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False)
    image = db.Column(db.String(400))
    products = db.relationship("Product", backref="category")
    subcategories = db.relationship("SubCategory", backref="category")


class SubCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    products = db.relationship("Product", backref="subcategory")


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False)
    image = db.Column(db.String(400))
    products = db.relationship("Product", backref="brand")


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(220), unique=True, nullable=False)
    description = db.Column(db.Text, default="")
    image = db.Column(db.String(400))
    price = db.Column(db.Float, nullable=False)
    compare_at = db.Column(db.Float)
    stock = db.Column(db.Integer, default=50)
    sold = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=False)
    is_flash = db.Column(db.Boolean, default=False)
    is_bestseller = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    subcategory_id = db.Column(db.Integer, db.ForeignKey("sub_category.id"))
    brand_id = db.Column(db.Integer, db.ForeignKey("brand.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship("Review", backref="product", cascade="all, delete-orphan")

    @property
    def discount_percent(self):
        if self.compare_at and self.compare_at > self.price:
            return int(round((1 - self.price / self.compare_at) * 100))
        return 0

    @property
    def in_stock(self):
        return self.stock > 0


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship("Product")


class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    product = db.relationship("Product")
    __table_args__ = (db.UniqueConstraint("user_id", "product_id"),)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    order_number = db.Column(db.String(24), unique=True, nullable=False)
    status = db.Column(db.String(40), default="pending")
    payment_method = db.Column(db.String(40), default="cod")
    subtotal = db.Column(db.Float, default=0)
    shipping = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    shipping_name = db.Column(db.String(120))
    shipping_phone = db.Column(db.String(40))
    shipping_address = db.Column(db.String(300))
    shipping_city = db.Column(db.String(80))
    note = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship("OrderItem", backref="order", cascade="all, delete-orphan")


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    image = db.Column(db.String(400))


class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    image = db.Column(db.String(400))
    link = db.Column(db.String(300), default="#")
    sort_order = db.Column(db.Integer, default=0)


class Promo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    image = db.Column(db.String(400))
    link = db.Column(db.String(300), default="#")
