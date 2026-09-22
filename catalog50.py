from flask import redirect
from sqlalchemy import text

ITEMS = [
    ("iPhone 13 Pro", "https://cdn.dummyjson.com/product-images/smartphones/iphone-13-pro/thumbnail.webp"),
    ("iPhone X", "https://cdn.dummyjson.com/product-images/smartphones/iphone-x/thumbnail.webp"),
    ("iPhone 6", "https://cdn.dummyjson.com/product-images/smartphones/iphone-6/thumbnail.webp"),
    ("Samsung Galaxy S10", "https://cdn.dummyjson.com/product-images/smartphones/samsung-galaxy-s10/thumbnail.webp"),
    ("Samsung Galaxy S8", "https://cdn.dummyjson.com/product-images/smartphones/samsung-galaxy-s8/thumbnail.webp"),
    ("Samsung Galaxy S7", "https://cdn.dummyjson.com/product-images/smartphones/samsung-galaxy-s7/thumbnail.webp"),
    ("Oppo F19 Pro Plus", "https://cdn.dummyjson.com/product-images/smartphones/oppo-f19-pro-plus/thumbnail.webp"),
    ("Oppo A57", "https://cdn.dummyjson.com/product-images/smartphones/oppo-a57/thumbnail.webp"),
    ("Realme XT", "https://cdn.dummyjson.com/product-images/smartphones/realme-xt/thumbnail.webp"),
    ("Vivo X21", "https://cdn.dummyjson.com/product-images/smartphones/vivo-x21/thumbnail.webp"),
    ("MacBook Pro 14", "https://cdn.dummyjson.com/product-images/laptops/apple-macbook-pro-14-inch-space-grey/thumbnail.webp"),
    ("Dell XPS 13", "https://cdn.dummyjson.com/product-images/laptops/new-dell-xps-13-9300-laptop/thumbnail.webp"),
    ("Huawei MateBook X Pro", "https://cdn.dummyjson.com/product-images/laptops/huawei-matebook-x-pro/thumbnail.webp"),
    ("Lenovo Yoga 920", "https://cdn.dummyjson.com/product-images/laptops/lenovo-yoga-920/thumbnail.webp"),
    ("Asus Zenbook Pro", "https://cdn.dummyjson.com/product-images/laptops/asus-zenbook-pro-dual-screen-laptop/thumbnail.webp"),
    ("iPad Mini", "https://cdn.dummyjson.com/product-images/tablets/ipad-mini-2021-starlight/thumbnail.webp"),
    ("Galaxy Tab S8+", "https://cdn.dummyjson.com/product-images/tablets/samsung-galaxy-tab-s8-plus-grey/thumbnail.webp"),
    ("Galaxy Tab White", "https://cdn.dummyjson.com/product-images/tablets/samsung-galaxy-tab-white/thumbnail.webp"),
    ("Apple AirPods", "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods/thumbnail.webp"),
    ("AirPods Max Silver", "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods-max-silver/thumbnail.webp"),
    ("Beats Flex Earphones", "https://cdn.dummyjson.com/product-images/mobile-accessories/beats-flex-wireless-earphones/thumbnail.webp"),
    ("Apple Watch Series 4", "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-watch-series-4-gold/thumbnail.webp"),
    ("iPhone Charger", "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-iphone-charger/thumbnail.webp"),
    ("MagSafe Battery Pack", "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-magsafe-battery-pack/thumbnail.webp"),
    ("AirPower Charger", "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpower-wireless-charger/thumbnail.webp"),
    ("HomePod Mini", "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-homepod-mini-cosmic-grey/thumbnail.webp"),
    ("Echo Plus", "https://cdn.dummyjson.com/product-images/mobile-accessories/amazon-echo-plus/thumbnail.webp"),
    ("iPhone 12 Silicone Case", "https://cdn.dummyjson.com/product-images/mobile-accessories/iphone-12-silicone-case-with-magsafe-plum/thumbnail.webp"),
    ("Selfie Stick", "https://cdn.dummyjson.com/product-images/mobile-accessories/selfie-stick-monopod/thumbnail.webp"),
    ("Monopod", "https://cdn.dummyjson.com/product-images/mobile-accessories/monopod/thumbnail.webp"),
    ("Rolex Datejust", "https://cdn.dummyjson.com/product-images/mens-watches/rolex-datejust/thumbnail.webp"),
    ("Rolex Submariner", "https://cdn.dummyjson.com/product-images/mens-watches/rolex-submariner-watch/thumbnail.webp"),
    ("Rolex Cellini Date", "https://cdn.dummyjson.com/product-images/mens-watches/rolex-cellini-date-black-dial/thumbnail.webp"),
    ("Longines Master", "https://cdn.dummyjson.com/product-images/mens-watches/longines-master-collection/thumbnail.webp"),
    ("Leather Belt Watch", "https://cdn.dummyjson.com/product-images/mens-watches/brown-leather-belt-watch/thumbnail.webp"),
    ("Nike Air Jordan 1", "https://cdn.dummyjson.com/product-images/mens-shoes/nike-air-jordan-1-red-and-black/thumbnail.webp"),
    ("Puma Future Rider", "https://cdn.dummyjson.com/product-images/mens-shoes/puma-future-rider-trainers/thumbnail.webp"),
    ("Sports Sneakers", "https://cdn.dummyjson.com/product-images/mens-shoes/sports-sneakers-off-white-red/thumbnail.webp"),
    ("Classic Sunglasses", "https://cdn.dummyjson.com/product-images/sunglasses/classic-sun-glasses/thumbnail.webp"),
    ("Black Sunglasses", "https://cdn.dummyjson.com/product-images/sunglasses/black-sun-glasses/thumbnail.webp"),
    ("Prada Bag", "https://cdn.dummyjson.com/product-images/womens-bags/prada-women-bag/thumbnail.webp"),
    ("Leather Handbag", "https://cdn.dummyjson.com/product-images/womens-bags/heshe-women's-leather-bag/thumbnail.webp"),
    ("Black Handbag", "https://cdn.dummyjson.com/product-images/womens-bags/women-handbag-black/thumbnail.webp"),
    ("Blue Handbag", "https://cdn.dummyjson.com/product-images/womens-bags/blue-women's-handbag/thumbnail.webp"),
    ("White Backpack", "https://cdn.dummyjson.com/product-images/womens-bags/white-faux-leather-backpack/thumbnail.webp"),
    ("Oppo K1", "https://cdn.dummyjson.com/product-images/smartphones/oppo-k1/thumbnail.webp"),
    ("Realme C35", "https://cdn.dummyjson.com/product-images/smartphones/realme-c35/thumbnail.webp"),
    ("Vivo S1", "https://cdn.dummyjson.com/product-images/smartphones/vivo-s1/thumbnail.webp"),
    ("Vivo V9", "https://cdn.dummyjson.com/product-images/smartphones/vivo-v9/thumbnail.webp"),
    ("Realme X", "https://cdn.dummyjson.com/product-images/smartphones/realme-x/thumbnail.webp"),
]

CATS = {
    "computer": "https://cdn.dummyjson.com/product-images/laptops/apple-macbook-pro-14-inch-space-grey/thumbnail.webp",
    "smart": "https://cdn.dummyjson.com/product-images/smartphones/iphone-13-pro/thumbnail.webp",
    "head": "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-airpods-max-silver/thumbnail.webp",
    "access": "https://cdn.dummyjson.com/product-images/mobile-accessories/apple-iphone-charger/thumbnail.webp",
    "camera": "https://cdn.dummyjson.com/product-images/mobile-accessories/monopod/thumbnail.webp",
    "tv": "https://cdn.dummyjson.com/product-images/mobile-accessories/amazon-echo-plus/thumbnail.webp",
    "fashion": "https://cdn.dummyjson.com/product-images/mens-shoes/nike-air-jordan-1-red-and-black/thumbnail.webp",
}


def _wipe_products():
    from extensions import db
    for tbl in ("cart_item", "order_item", "wishlist_item"):
        try:
            db.session.execute(text("DELETE FROM " + tbl))
            db.session.commit()
        except Exception:
            db.session.rollback()
    from models import Product
    try:
        Product.query.delete()
        db.session.commit()
    except Exception:
        db.session.rollback()
        for p in Product.query.all():
            db.session.delete(p)
        db.session.commit()


def apply_pack():
    from extensions import db
    from models import Product, Category
    from catalog import clear_catalog
    _wipe_products()
    cat = Category.query.first()
    cat_id = cat.id if cat else None
    for i, (name, image) in enumerate(ITEMS):
        db.session.add(Product(
            name=name,
            slug="w50-%02d" % (i + 1),
            description=name,
            image=image,
            price=float(129 + i * 37),
            stock=50,
            category_id=cat_id,
        ))
    for c in Category.query.all():
        key = (c.name or "").lower()
        img = None
        if "computer" in key or "laptop" in key:
            img = CATS["computer"]
        elif "smart" in key or "phone" in key:
            img = CATS["smart"]
        elif "head" in key:
            img = CATS["head"]
        elif "access" in key:
            img = CATS["access"]
        elif "camera" in key:
            img = CATS["camera"]
        elif "tv" in key or "home" in key:
            img = CATS["tv"]
        elif "fashion" in key:
            img = CATS["fashion"]
        if img:
            c.image = img
    db.session.commit()
    clear_catalog()
    return "reset"


def install_catalog50(app):
    if getattr(app, "_c50", False):
        return
    app._c50 = True

    @app.before_request
    def _load_pack():
        try:
            from models import Product
            n = Product.query.filter(Product.slug.like("w50-%")).count()
            junk = Product.query.filter(Product.name.in_(["HD Webcam", "Mechanical Keyboard", "Wireless Mouse"])).first()
            if n < 40 or junk:
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
        return redirect("/shop")
