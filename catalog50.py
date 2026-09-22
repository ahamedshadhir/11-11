from flask import redirect

# DummyJSON packshots — product-only, light / white studio
SHOTS = [
    "https://cdn.dummyjson.com/product-images/smartphones/iphone-13-pro/1.webp",
    "https://cdn.dummyjson.com/product-images/smartphones/iphone-x/1.webp",
    "https://cdn.dummyjson.com/product-images/smartphones/samsung-galaxy-s8/1.webp",
    "https://cdn.dummyjson.com/product-images/laptops/macbook-pro/1.webp",
    "https://cdn.dummyjson.com/product-images/laptops/huawei-matebook-x-pro/1.webp",
    "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods/1.webp",
    "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods-max-silver/1.webp",
    "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpower-wireless-charger/1.webp",
    "https://cdn.dummyjson.com/product-images/mens-watches/brown-leather-belt-watch/1.webp",
    "https://cdn.dummyjson.com/product-images/mens-watches/longines-master-collection/1.webp",
    "https://cdn.dummyjson.com/product-images/mens-shoes/nike-air-jordan-1-red-and-black/1.webp",
    "https://cdn.dummyjson.com/product-images/mens-shoes/nike-baseball-cleats/1.webp",
    "https://cdn.dummyjson.com/product-images/womens-bags/prada-prada-galleria-satin-mini-bag/1.webp",
    "https://cdn.dummyjson.com/product-images/sunglasses/classic-gold-frames/1.webp",
    "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-magsafe-wallet-salmon/1.webp",
    "https://cdn.dummyjson.com/product-images/tablets/ipad-mini-2021-starlight/1.webp",
    "https://cdn.dummyjson.com/product-images/smartphones/iphone-5s/1.webp",
    "https://cdn.dummyjson.com/product-images/laptops/dummy-json-lenovo-ideapad-720s/1.webp",
    "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods-max-silver/2.webp",
    "https://cdn.dummyjson.com/product-images/mens-watches/rolex-cellini-date-black-dial/1.webp",
]

NAMES = [
    "iPhone 15", "Galaxy S24", "Pixel 8", "MacBook Air 13", "ThinkPad X1",
    "Studio Headphones", "Wireless Over-Ear", "True Wireless Buds", "Field Watch", "Sport Watch",
    "Runner Sneaker", "Court Sneaker", "Leather Crossbody", "Aviator Sunglasses", "MagSafe Wallet",
    "iPad mini", "iPhone SE", "Yoga Slim 7", "AirPods Max", "Dress Watch",
    "iPhone 15 Plus", "Galaxy A55", "Pixel 8a", "MacBook Pro 14", "MateBook",
    "Noise-Cancel Headphones", "On-Ear Headset", "Sport Earbuds", "Leather Watch", "Master Watch",
    "Trail Sneaker", "Canvas Sneaker", "Mini Shoulder Bag", "Gold Frames", "Phone Case",
    "iPad Air", "Laptop Sleeve", "USB-C Hub", "MagSafe Charger", "Power Bank 20K",
    "Bluetooth Speaker", "Action Camera", "Wireless Mouse", "Mechanical Keyboard", "HD Webcam",
    "Galaxy Tab", "Silicone Case", "Instant Camera", "Round Sunglasses", "Smart Band",
]


def apply_pack():
    from extensions import db
    from models import Product, Category
    from catalog import clear_catalog
    cat = Category.query.first()
    cat_id = cat.id if cat else None
    rows = Product.query.order_by(Product.id).all()
    if len(rows) < 20:
        for i, name in enumerate(NAMES):
            slug = "w50-%02d" % (i + 1)
            if Product.query.filter_by(slug=slug).first():
                continue
            db.session.add(Product(
                name=name,
                slug=slug,
                description="Studio packshot on white.",
                image=SHOTS[i % len(SHOTS)],
                price=float(89 + (i * 37) % 2400),
                compare_at=float(169 + (i * 37) % 2400),
                stock=50,
                category_id=cat_id,
            ))
        db.session.commit()
        rows = Product.query.order_by(Product.id).all()
    for i, p in enumerate(rows):
        p.image = SHOTS[i % len(SHOTS)]
    db.session.commit()
    clear_catalog()
    return "white"


def install_catalog50(app):
    if getattr(app, "_c50", False):
        return
    app._c50 = True

    @app.before_request
    def _load_pack():
        try:
            from models import Product
            p = Product.query.first()
            if (not p) or (p.image and "dummyjson.com" not in (p.image or "")):
                apply_pack()
        except Exception:
            try:
                from extensions import db
                db.session.rollback()
            except Exception:
                pass

    @app.route("/__reseed")
    def reseed_catalog():
        try:
            apply_pack()
        except Exception:
            pass
        return redirect("/admin/products")
