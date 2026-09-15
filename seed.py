from models import db, User, Category, SubCategory, Brand, Product, Banner, Promo

IMG = {
    'laptop': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80',
    'gaming_laptop': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=900&q=80',
    'phone': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=900&q=80',
    'iphone': 'https://images.unsplash.com/photo-1591337676887-a217a6970a8a?auto=format&fit=crop&w=900&q=80',
    'pixel': 'https://images.unsplash.com/photo-1598327105666-5b89391faea5?auto=format&fit=crop&w=900&q=80',
    'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80',
    'xm5': 'https://images.unsplash.com/photo-1546435770-a3e426b576d7?auto=format&fit=crop&w=900&q=80',
    'earbuds': 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=900&q=80',
    'case': 'https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?auto=format&fit=crop&w=900&q=80',
    'charger': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=900&q=80',
    'powerbank': 'https://images.unsplash.com/photo-1609091839311-d5369f2b0b5b?auto=format&fit=crop&w=900&q=80',
    'camera': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80',
    'tripod': 'https://images.unsplash.com/photo-1495707902641-75cac588d2e9?auto=format&fit=crop&w=900&q=80',
    'tv': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=900&q=80',
    'theatre': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=900&q=80',
    'sneakers_w': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=900&q=80',
    'sneakers_b': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80',
    'bag': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=900&q=80',
    'watch': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80',
    'cat_comp': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=500&q=80',
    'cat_phone': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=500&q=80',
    'cat_head': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80',
    'cat_acc': 'https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?auto=format&fit=crop&w=500&q=80',
    'cat_cam': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=500&q=80',
    'cat_tv': 'https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=500&q=80',
    'cat_fashion': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=500&q=80',
    'banner1': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=1600&q=80',
    'banner2': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=1600&q=80',
    'banner3': 'https://images.unsplash.com/photo-1483985988355-763728e1935b?auto=format&fit=crop&w=1600&q=80',
    'promo1': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=1000&q=80',
    'promo2': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=1000&q=80',
    'brand': 'https://images.unsplash.com/photo-1560393464-5c69a73c5770?auto=format&fit=crop&w=400&q=80',
}


def _upsert(model, match, **fields):
    row = model.query.filter_by(**match).first()
    if row is None:
        row = model(**match, **fields)
        db.session.add(row)
    else:
        for key, value in fields.items():
            setattr(row, key, value)
    return row


def ensure_users(app):
    rows = [
        (app.config['ADMIN_EMAIL'], 'Store Admin', app.config['ADMIN_PASSWORD'], True),
        ('demo@1111.local', 'Aisha Al-Thani', 'demo123', False),
    ]
    for email, name, pw, admin in rows:
        u = User.query.filter_by(email=email).first()
        if not u:
            u = User(name=name, email=email, is_admin=admin)
            db.session.add(u)
        u.name = name
        u.set_password(pw)
        u.is_admin = bool(admin)
    db.session.commit()


def seed_all(app):
    """Always upsert catalog so Vercel /tmp (and Neon) pick up QAR price fixes."""
    with app.app_context():
        ensure_users(app)

        cats = [
            dict(id=2, name='Computer & Laptop', slug='computer-laptop', image=IMG['cat_comp']),
            dict(id=3, name='SmartPhone', slug='smartphone', image=IMG['cat_phone']),
            dict(id=4, name='Headphones', slug='headphones', image=IMG['cat_head']),
            dict(id=5, name='Accessories', slug='accessories', image=IMG['cat_acc']),
            dict(id=6, name='Camera & Photo', slug='camera-photo', image=IMG['cat_cam']),
            dict(id=7, name='TV & Homes', slug='tv-homes', image=IMG['cat_tv']),
            dict(id=8, name='Fashion', slug='fashion', image=IMG['cat_fashion']),
        ]
        for row in cats:
            cid = row.pop('id')
            existing = db.session.get(Category, cid) or Category.query.filter_by(slug=row['slug']).first()
            if existing is None:
                db.session.add(Category(id=cid, **row))
            else:
                for k, v in row.items():
                    setattr(existing, k, v)

        subs = [
            dict(id=5, name='Desktop Computers', slug='desktop-computers', category_id=2),
            dict(id=6, name='Gaming Laptops', slug='gaming-laptops', category_id=2),
            dict(id=19, name='Ultrabooks', slug='ultrabooks', category_id=2),
            dict(id=7, name='Android Phones', slug='android-phones', category_id=3),
            dict(id=8, name='iPhones', slug='iphones', category_id=3),
            dict(id=9, name='Wireless Headphones', slug='wireless-headphones', category_id=4),
            dict(id=10, name='Earbuds', slug='earbuds', category_id=4),
            dict(id=11, name='Phone Cases', slug='phone-cases', category_id=5),
            dict(id=12, name='Chargers', slug='chargers', category_id=5),
            dict(id=13, name='Power Banks', slug='power-banks', category_id=5),
            dict(id=14, name='DSLR Cameras', slug='dslr-cameras', category_id=6),
            dict(id=15, name='Tripods', slug='tripods', category_id=6),
            dict(id=16, name='Smart TVs', slug='smart-tvs', category_id=7),
            dict(id=17, name='Home Theatre', slug='home-theatre', category_id=7),
            dict(id=18, name='Sneakers', slug='sneakers', category_id=8),
            dict(id=20, name='Bags', slug='bags', category_id=8),
            dict(id=21, name='Watches', slug='watches', category_id=8),
        ]
        for row in subs:
            sid = row.pop('id')
            existing = db.session.get(SubCategory, sid) or SubCategory.query.filter_by(slug=row['slug']).first()
            if existing is None:
                db.session.add(SubCategory(id=sid, **row))
            else:
                for k, v in row.items():
                    setattr(existing, k, v)

        brands = [
            dict(id=1, name='Samsung', slug='samsung'),
            dict(id=2, name='D&G', slug='dg'),
            dict(id=3, name='H&M', slug='hm'),
            dict(id=4, name='LV', slug='lv'),
            dict(id=5, name='Prada', slug='prada'),
            dict(id=6, name='Apple', slug='apple'),
            dict(id=7, name='Sony', slug='sony'),
            dict(id=8, name='Gucci', slug='gucci'),
            dict(id=9, name='Nike', slug='nike'),
            dict(id=10, name='Canon', slug='canon'),
            dict(id=11, name='Google', slug='google'),
        ]
        for row in brands:
            bid = row.pop('id')
            existing = db.session.get(Brand, bid) or Brand.query.filter_by(slug=row['slug']).first()
            fields = dict(row, image=IMG['brand'])
            if existing is None:
                db.session.add(Brand(id=bid, **fields))
            else:
                for k, v in fields.items():
                    setattr(existing, k, v)
        db.session.flush()

        old_s23 = Product.query.filter_by(slug='samsung-galaxy-s23').first()
        if old_s23 and not Product.query.filter_by(slug='samsung-galaxy-s24').first():
            old_s23.slug = 'samsung-galaxy-s24'
            db.session.flush()

        products = [
            dict(slug='samsung-galaxy-s24', name='Samsung Galaxy S24', description='Flagship Android with a bright AMOLED display, 50MP camera and all-day battery. Dual SIM, 256GB.', image=IMG['phone'], price=3299, compare_at=3799, stock=44, sold=91, rating=4.6, review_count=28, is_featured=True, is_flash=True, is_bestseller=True, category_id=3, subcategory_id=7, brand_id=1),
            dict(slug='iphone-15-pro', name='iPhone 15 Pro', description='Titanium iPhone with A17 Pro, 48MP camera and USB-C. 256GB.', image=IMG['iphone'], price=4899, compare_at=5299, stock=25, sold=40, rating=4.8, review_count=32, is_featured=True, is_flash=False, is_bestseller=True, category_id=3, subcategory_id=8, brand_id=6),
            dict(slug='google-pixel-8', name='Google Pixel 8', description='Clean Android, best-in-class computational photography, 7 years of updates.', image=IMG['pixel'], price=2499, compare_at=2899, stock=30, sold=18, rating=4.5, review_count=14, is_featured=True, is_flash=False, is_bestseller=False, category_id=3, subcategory_id=7, brand_id=11),
            dict(slug='macbook-air-13', name='MacBook Air 13', description='M3 ultrabook. Silent, light, all-day battery. 16GB / 512GB, midnight.', image=IMG['laptop'], price=4499, compare_at=4999, stock=18, sold=21, rating=4.7, review_count=14, is_featured=True, is_flash=False, is_bestseller=True, category_id=2, subcategory_id=19, brand_id=6),
            dict(slug='macbook-pro-14', name='MacBook Pro 14', description='M3 Pro for editors and developers. Liquid Retina XDR, 18GB unified memory.', image=IMG['laptop'], price=7299, compare_at=7999, stock=9, sold=11, rating=4.9, review_count=9, is_featured=True, is_flash=False, is_bestseller=False, category_id=2, subcategory_id=19, brand_id=6),
            dict(slug='16-inch-gaming-laptop', name='16-inch Gaming Laptop', description='144Hz panel, RTX-class graphics, RGB keyboard. Built for Lusail LAN nights.', image=IMG['gaming_laptop'], price=5199, compare_at=5899, stock=12, sold=16, rating=4.4, review_count=11, is_featured=False, is_flash=True, is_bestseller=False, category_id=2, subcategory_id=6, brand_id=7),
            dict(slug='wireless-over-ear', name='Wireless Over-Ear Headphones', description='Adaptive ANC, 30-hour battery, plush ear cups. Fold-flat case included.', image=IMG['headphones'], price=899, compare_at=1199, stock=40, sold=63, rating=4.6, review_count=28, is_featured=True, is_flash=True, is_bestseller=True, category_id=4, subcategory_id=9, brand_id=7),
            dict(slug='sony-wh-1000xm5', name='Sony WH-1000XM5', description='Industry-leading noise cancelling, Speak-to-Chat, multipoint Bluetooth.', image=IMG['xm5'], price=1299, compare_at=1499, stock=22, sold=34, rating=4.8, review_count=41, is_featured=True, is_flash=False, is_bestseller=True, category_id=4, subcategory_id=9, brand_id=7),
            dict(slug='airpods-pro', name='AirPods Pro', description='USB-C AirPods Pro with Adaptive Audio and MagSafe case.', image=IMG['earbuds'], price=899, compare_at=999, stock=55, sold=120, rating=4.7, review_count=64, is_featured=False, is_flash=False, is_bestseller=True, category_id=4, subcategory_id=10, brand_id=6),
            dict(slug='galaxy-buds3', name='Galaxy Buds3', description='Compact ANC earbuds with wireless charging case and IP57 rating.', image=IMG['earbuds'], price=449, compare_at=549, stock=70, sold=88, rating=4.3, review_count=19, is_featured=False, is_flash=False, is_bestseller=False, category_id=4, subcategory_id=10, brand_id=1),
            dict(slug='clear-phone-case', name='Clear Phone Case', description='Slim MagSafe-ready case. Anti-yellowing TPU, raised camera lip.', image=IMG['case'], price=49, compare_at=79, stock=200, sold=310, rating=4.1, review_count=18, is_featured=False, is_flash=False, is_bestseller=False, category_id=5, subcategory_id=11, brand_id=3),
            dict(slug='fast-wall-charger-65w', name='Fast Wall Charger 65W', description='GaN charger, two USB-C ports. Phone + laptop from one brick.', image=IMG['charger'], price=129, compare_at=179, stock=90, sold=55, rating=4.4, review_count=11, is_featured=False, is_flash=True, is_bestseller=False, category_id=5, subcategory_id=12, brand_id=6),
            dict(slug='20000mah-power-bank', name='20,000mAh Power Bank', description='PD 30W in and out. Two full phone charges, airline-safe.', image=IMG['powerbank'], price=149, compare_at=199, stock=80, sold=140, rating=4.5, review_count=22, is_featured=False, is_flash=False, is_bestseller=True, category_id=5, subcategory_id=13, brand_id=1),
            dict(slug='canon-eos-r50', name='Canon EOS R50', description='Mirrorless 24MP with 18-45mm kit lens. 4K video, flip screen.', image=IMG['camera'], price=2799, compare_at=3199, stock=14, sold=9, rating=4.6, review_count=8, is_featured=True, is_flash=False, is_bestseller=False, category_id=6, subcategory_id=14, brand_id=10),
            dict(slug='travel-tripod', name='Travel Tripod', description='Carbon-look aluminum, 1.6kg, arca-swiss plate. Fits a cabin bag.', image=IMG['tripod'], price=189, compare_at=249, stock=36, sold=27, rating=4.2, review_count=7, is_featured=False, is_flash=False, is_bestseller=False, category_id=6, subcategory_id=15, brand_id=7),
            dict(slug='55-inch-4k-smart-tv', name='55-inch 4K Smart TV', description='4K HDR, 120Hz motion, built-in apps. Slim bezels for a West Bay lounge.', image=IMG['tv'], price=1899, compare_at=2299, stock=14, sold=22, rating=4.4, review_count=16, is_featured=True, is_flash=False, is_bestseller=False, category_id=7, subcategory_id=16, brand_id=1),
            dict(slug='65-inch-oled-tv', name='65-inch OLED TV', description='Self-lit OLED, Dolby Vision, 4 HDMI 2.1 ports for consoles.', image=IMG['tv'], price=4499, compare_at=5299, stock=7, sold=6, rating=4.9, review_count=5, is_featured=True, is_flash=False, is_bestseller=False, category_id=7, subcategory_id=16, brand_id=7),
            dict(slug='31-soundbar', name='3.1 Soundbar', description='Wireless sub, HDMI eARC, DTS Virtual:X. Fills a Pearl apartment.', image=IMG['theatre'], price=799, compare_at=999, stock=20, sold=15, rating=4.3, review_count=10, is_featured=False, is_flash=False, is_bestseller=False, category_id=7, subcategory_id=17, brand_id=7),
            dict(slug='white-sneakers', name='White Court Sneakers', description='Full-grain leather, cushioned insole, gum sole. Everyday Doha white.', image=IMG['sneakers_w'], price=199, compare_at=249, stock=48, sold=56, rating=4.9, review_count=12, is_featured=True, is_flash=True, is_bestseller=True, category_id=8, subcategory_id=18, brand_id=9),
            dict(slug='black-running-sneakers', name='Black Running Sneakers', description='Breathable mesh, responsive foam, 8mm drop. For Corniche loops.', image=IMG['sneakers_b'], price=349, compare_at=429, stock=60, sold=33, rating=4.4, review_count=9, is_featured=True, is_flash=True, is_bestseller=True, category_id=8, subcategory_id=18, brand_id=9),
            dict(slug='leather-crossbody', name='Leather Crossbody', description='Structured calf leather, detachable strap, suede lining.', image=IMG['bag'], price=459, compare_at=599, stock=18, sold=12, rating=4.5, review_count=6, is_featured=False, is_flash=False, is_bestseller=False, category_id=8, subcategory_id=20, brand_id=8),
            dict(slug='classic-field-watch', name='Classic Field Watch', description='Sapphire crystal, 40mm case, 10ATM. Quiet gold indices.', image=IMG['watch'], price=890, compare_at=1100, stock=15, sold=8, rating=4.6, review_count=4, is_featured=True, is_flash=False, is_bestseller=False, category_id=8, subcategory_id=21, brand_id=5),
        ]
        for row in products:
            _upsert(Product, {'slug': row.pop('slug')}, **row)
        db.session.flush()

        if Banner.query.count() == 0:
            db.session.add_all([
                Banner(title='Shoes Sale', image=IMG['banner1'], link='/shop?category=8', sort_order=1),
                Banner(title='Brand offer', image=IMG['banner2'], link='/shop?brand=1', sort_order=2),
                Banner(title='Seasonal Offers', image=IMG['banner3'], link='/shop', sort_order=3),
            ])
        if Promo.query.count() == 0:
            db.session.add_all([
                Promo(title='Headphones', image=IMG['promo1'], link='/shop?category=4'),
                Promo(title='Products', image=IMG['promo2'], link='/shop?brand=7'),
            ])
        db.session.commit()
