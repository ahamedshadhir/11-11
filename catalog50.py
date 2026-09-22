from flask import redirect

PHOTOS = [
    "images.unsplash.com/photo-1510557880182-3d4d3cba35a5",
    "images.unsplash.com/photo-1511707171634-5f897ff02aa9",
    "images.unsplash.com/photo-1592899677977-9c10ca588bbd",
    "images.unsplash.com/photo-1517336714731-489689fd1ca8",
    "images.unsplash.com/photo-1496181133206-80ce9b88a853",
    "images.unsplash.com/photo-1484704849700-f032a568e944",
    "images.unsplash.com/photo-1505740420928-5e560c06d30e",
    "images.unsplash.com/photo-1590658268037-6bf12165a8df",
    "images.unsplash.com/photo-1523275335684-37898b6baf30",
    "images.unsplash.com/photo-1546868871-7041f2af46e7",
    "images.unsplash.com/photo-1542291026-7eec264c27ff",
    "images.unsplash.com/photo-1549298916-b41d501d3772",
    "images.unsplash.com/photo-1584917865442-de89df76afd3",
    "images.unsplash.com/photo-1572635196237-14b3f2816fef",
    "images.unsplash.com/photo-1516035069371-29a1b244cc32",
    "images.unsplash.com/photo-1593359677879-a4bb92f829d1",
    "images.unsplash.com/photo-1601784551446-20c9e07cdbdb",
    "images.unsplash.com/photo-1610945415295-d9bbf067e59c",
    "images.unsplash.com/photo-1526170375885-4d8ecf77b99f",
    "images.unsplash.com/photo-1572635196184-84e35138cf62",
]

NAMES = [
    "iPhone 15", "Galaxy S24", "Pixel 8", "MacBook Air 13", "ThinkPad X1",
    "Studio Headphones", "Wireless Over-Ear", "True Wireless Buds", "Field Watch", "Sport Watch",
    "Runner Sneaker", "Court Sneaker", "Leather Crossbody", "Aviator Sunglasses", "Mirrorless Camera",
    "4K Smart TV", "Clear Phone Case", "Galaxy Flip", "Polaroid Camera", "Classic Shades",
    "iPhone 15 Plus", "Galaxy A55", "Pixel 8a", "MacBook Pro 14", "Yoga Slim 7",
    "Noise-Cancel Headphones", "On-Ear Headset", "Sport Earbuds", "Dress Watch", "Smart Band",
    "Trail Sneaker", "Canvas Sneaker", "Mini Shoulder Bag", "Wayfarer Sunglasses", "Compact Camera",
    "55-inch LED TV", "Silicone Case", "Galaxy Tab", "Instant Camera", "Round Sunglasses",
    "iPad Air", "Laptop Sleeve", "USB-C Hub", "MagSafe Charger", "Power Bank 20K",
    "Bluetooth Speaker", "Action Camera", "Wireless Mouse", "Mechanical Keyboard", "HD Webcam",
]


def pack(i):
    return "https://images.weserv.nl/?url=" + PHOTOS[i % len(PHOTOS)] + "&bg=ffffff&fit=contain&w=800&h=800"


def apply_pack():
    from extensions import db
    from models import Product, Category
    from catalog import clear_catalog
    cat = Category.query.first()
    cat_id = cat.id if cat else None
    if Product.query.count() >= 40:
        return "ok"
    for i, name in enumerate(NAMES):
        slug = "w50-%02d" % (i + 1)
        if Product.query.filter_by(slug=slug).first():
            continue
        db.session.add(Product(
            name=name,
            slug=slug,
            description="Studio photo on white.",
            image=pack(i),
            price=float(89 + (i * 37) % 2400),
            compare_at=float(169 + (i * 37) % 2400),
            stock=50,
            category_id=cat_id,
        ))
    db.session.commit()
    clear_catalog()
    return "seeded"


def install_catalog50(app):
    if getattr(app, "_c50", False):
        return
    app._c50 = True

    @app.before_request
    def _load_pack():
        try:
            from models import Product
            if Product.query.count() < 20:
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
