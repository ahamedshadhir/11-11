from models import db, User, Category, SubCategory, Brand, Product, Banner, Promo, Review

IMG = {
    'laptop': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80',
    'gaming_laptop': 'https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=900&q=80',
    'desktop': 'https://images.unsplash.com/photo-1593640408182-31c70c8269f5?auto=format&fit=crop&w=900&q=80',
    'phone': 'https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?auto=format&fit=crop&w=900&q=80',
    'iphone': 'https://images.unsplash.com/photo-1591337676887-a217a6970a8a?auto=format&fit=crop&w=900&q=80',
    'android': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=80',
    'headphones': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80',
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
    'sneakers_w2': 'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?auto=format&fit=crop&w=900&q=80',
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
        u.set_password(pw)
        u.is_admin = bool(admin)
    db.session.commit()

def seed_all(app):
    with app.app_context():
        if Product.query.count() > 0:
            ensure_users(app)
            return
        admin = User(name='Store Admin', email=app.config['ADMIN_EMAIL'], is_admin=True)
        admin.set_password(app.config['ADMIN_PASSWORD'])
        demo = User(name='Aisha Al-Thani', email='demo@1111.local')
        demo.set_password('demo123')
        db.session.add_all([admin, demo])
        db.session.flush()
        db.session.add_all([
            Category(id=2, name='Computer & Laptop', slug='computer-laptop', image=IMG['cat_comp']),
            Category(id=3, name='SmartPhone', slug='smartphone', image=IMG['cat_phone']),
            Category(id=4, name='Headphones', slug='headphones', image=IMG['cat_head']),
            Category(id=5, name='Accessories', slug='accessories', image=IMG['cat_acc']),
            Category(id=6, name='Camera & Photo', slug='camera-photo', image=IMG['cat_cam']),
            Category(id=7, name='TV & Homes', slug='tv-homes', image=IMG['cat_tv']),
            Category(id=8, name='Fashion', slug='fashion', image=IMG['cat_fashion']),
        ])
        db.session.add_all([
            SubCategory(id=5, name='Desktop Computers', slug='desktop-computers', category_id=2),
            SubCategory(id=6, name='Gaming Laptops', slug='gaming-laptops', category_id=2),
            SubCategory(id=7, name='Android Phones', slug='android-phones', category_id=3),
            SubCategory(id=8, name='iPhones', slug='iphones', category_id=3),
            SubCategory(id=9, name='Wireless Headphones', slug='wireless-headphones', category_id=4),
            SubCategory(id=10, name='Earbuds', slug='earbuds', category_id=4),
            SubCategory(id=11, name='Phone Cases', slug='phone-cases', category_id=5),
            SubCategory(id=12, name='Chargers', slug='chargers', category_id=5),
            SubCategory(id=13, name='Power Banks', slug='power-banks', category_id=5),
            SubCategory(id=14, name='DSLR Cameras', slug='dslr-cameras', category_id=6),
            SubCategory(id=15, name='Tripods', slug='tripods', category_id=6),
            SubCategory(id=16, name='Smart TVs', slug='smart-tvs', category_id=7),
            SubCategory(id=17, name='Home Theatre', slug='home-theatre', category_id=7),
            SubCategory(id=18, name='Sneakers', slug='sneakers', category_id=8),
        ])
        db.session.add_all([
            Brand(id=1, name='Samsung', slug='samsung', image=IMG['brand']),
            Brand(id=2, name='D&G', slug='dg', image=IMG['brand']),
            Brand(id=3, name='H&M', slug='hm', image=IMG['brand']),
            Brand(id=4, name='LV', slug='lv', image=IMG['brand']),
            Brand(id=5, name='Prada', slug='prada', image=IMG['brand']),
            Brand(id=6, name='Apple', slug='apple', image=IMG['brand']),
            Brand(id=7, name='Sony', slug='sony', image=IMG['brand']),
            Brand(id=8, name='Gucci', slug='gucci', image=IMG['brand']),
            Brand(id=9, name='Nike', slug='nike', image=IMG['brand']),
        ])
        db.session.flush()
        db.session.add_all([
            Product(id=7, name='Samsung Galaxy S23', slug='samsung-galaxy-s23', description='Flagship Android phone.', image=IMG['phone'], price=95000, compare_at=120000, stock=44, sold=9, rating=3.2, review_count=2, is_featured=True, is_flash=True, is_bestseller=True, category_id=3, subcategory_id=7, brand_id=1),
            Product(id=8, name='White Sneakers', slug='white-sneakers', description='Everyday sneakers.', image=IMG['sneakers_w'], price=200, compare_at=250, stock=19, sold=56, rating=5.0, review_count=1, is_featured=True, is_flash=True, is_bestseller=True, category_id=8, subcategory_id=18, brand_id=9),
            Product(id=9, name='Black Running Sneakers', slug='black-running-sneakers', description='Running sneakers.', image=IMG['sneakers_b'], price=2999, compare_at=3500, stock=147, sold=3, rating=3.5, review_count=1, is_featured=True, is_flash=True, is_bestseller=True, category_id=8, subcategory_id=18, brand_id=9),
            Product(name='MacBook Air 13', slug='macbook-air-13', description='Ultra-portable laptop.', image=IMG['laptop'], price=4499, compare_at=4999, stock=18, sold=21, rating=4.7, review_count=14, is_featured=True, is_bestseller=True, category_id=2, subcategory_id=6, brand_id=6),
            Product(name='iPhone 15 Pro', slug='iphone-15-pro', description='Titanium iPhone.', image=IMG['iphone'], price=4899, compare_at=5299, stock=25, sold=40, rating=4.8, review_count=32, is_featured=True, category_id=3, subcategory_id=8, brand_id=6),
            Product(name='Wireless Over-Ear Headphones', slug='wireless-over-ear', description='ANC headphones.', image=IMG['headphones'], price=899, compare_at=1199, stock=40, sold=63, rating=4.6, review_count=28, is_featured=True, is_bestseller=True, category_id=4, subcategory_id=9, brand_id=7),
            Product(name='Clear Phone Case', slug='clear-phone-case', description='Slim case.', image=IMG['case'], price=49, compare_at=79, stock=200, sold=310, rating=4.1, review_count=18, category_id=5, subcategory_id=11, brand_id=3),
            Product(name='Fast Wall Charger 65W', slug='fast-wall-charger-65w', description='GaN charger.', image=IMG['charger'], price=129, compare_at=179, stock=90, sold=55, rating=4.4, review_count=11, category_id=5, subcategory_id=12, brand_id=6),
            Product(name='55-inch 4K Smart TV', slug='55-inch-4k-smart-tv', description='4K HDR TV.', image=IMG['tv'], price=1899, compare_at=2299, stock=14, sold=22, rating=4.4, review_count=16, is_featured=True, category_id=7, subcategory_id=16, brand_id=1),
        ])
        db.session.add_all([
            Banner(title='Shoes Sale', image=IMG['banner1'], link='/shop?category=8', sort_order=1),
            Banner(title='Brand offer', image=IMG['banner2'], link='/shop?brand=1', sort_order=2),
            Banner(title='Seasonal Offers', image=IMG['banner3'], link='/shop', sort_order=3),
            Promo(title='Headphones', image=IMG['promo1'], link='/shop?category=4'),
            Promo(title='Products', image=IMG['promo2'], link='/shop?brand=7'),
        ])
        db.session.commit()
