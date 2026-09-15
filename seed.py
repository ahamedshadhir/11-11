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

def seed_all(app):
    with app.app_context():
        if Product.query.count() > 0:
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
            Product(id=7, name='Samsung Galaxy S23', slug='samsung-galaxy-s23', description='Flagship Android phone with a triple camera system.', image=IMG['phone'], price=95000, compare_at=120000, stock=44, sold=9, rating=3.2, review_count=2, is_featured=True, is_flash=True, is_bestseller=True, category_id=3, subcategory_id=7, brand_id=1),
            Product(id=8, name='White Sneakers', slug='white-sneakers', description='Clean everyday sneakers with cushioned sole.', image=IMG['sneakers_w'], price=200, compare_at=250, stock=19, sold=56, rating=5.0, review_count=1, is_featured=True, is_flash=True, is_bestseller=True, category_id=8, subcategory_id=18, brand_id=9),
            Product(id=9, name='Black Running Sneakers', slug='black-running-sneakers', description='Performance running sneakers.', image=IMG['sneakers_b'], price=2999, compare_at=3500, stock=147, sold=3, rating=3.5, review_count=1, is_featured=True, is_flash=True, is_bestseller=True, category_id=8, subcategory_id=18, brand_id=9),
            Product(id=10, name='Ashish', slug='ashish', description='Everyday accessory pick from the 11-11 catalog.', image=IMG['watch'], price=5000, compare_at=5000, stock=30, sold=12, is_bestseller=True, category_id=5, subcategory_id=13, brand_id=3),
            Product(id=11, name='White sneaker', slug='white-sneaker', description='Minimal white sneaker with leather overlay.', image=IMG['sneakers_w2'], price=3500, compare_at=3999, stock=22, sold=8, is_bestseller=True, category_id=8, subcategory_id=18, brand_id=9),
            Product(id=12, name='Ultra Slim Gaming Laptop', slug='ultra-slim-gaming-laptop', description='Thin gaming laptop with dedicated GPU.', image=IMG['gaming_laptop'], price=79999, compare_at=85999, stock=11, sold=4, is_featured=True, is_bestseller=True, category_id=2, subcategory_id=6, brand_id=6),
            Product(name='MacBook Air 13', slug='macbook-air-13', description='Fanless ultra-portable laptop.', image=IMG['laptop'], price=4499, compare_at=4999, stock=18, sold=21, rating=4.7, review_count=14, is_featured=True, is_bestseller=True, category_id=2, subcategory_id=6, brand_id=6),
            Product(name='iPhone 15 Pro', slug='iphone-15-pro', description='Titanium iPhone with A17 Pro.', image=IMG['iphone'], price=4899, compare_at=5299, stock=25, sold=40, rating=4.8, review_count=32, is_featured=True, category_id=3, subcategory_id=8, brand_id=6),
            Product(name='Pixel 8', slug='pixel-8', description='Google Pixel with computational photography.', image=IMG['android'], price=2499, compare_at=2799, stock=16, sold=9, rating=4.5, review_count=7, category_id=3, subcategory_id=7, brand_id=1),
            Product(name='Wireless Over-Ear Headphones', slug='wireless-over-ear', description='ANC headphones with 30-hour battery.', image=IMG['headphones'], price=899, compare_at=1199, stock=40, sold=63, rating=4.6, review_count=28, is_featured=True, is_bestseller=True, category_id=4, subcategory_id=9, brand_id=7),
            Product(name='True Wireless Earbuds', slug='true-wireless-earbuds', description='Compact earbuds with ANC.', image=IMG['earbuds'], price=399, compare_at=549, stock=80, sold=120, rating=4.3, review_count=41, category_id=4, subcategory_id=10, brand_id=7),
            Product(name='Clear Phone Case', slug='clear-phone-case', description='Slim shock-absorbing case.', image=IMG['case'], price=49, compare_at=79, stock=200, sold=310, rating=4.1, review_count=18, category_id=5, subcategory_id=11, brand_id=3),
            Product(name='Fast Wall Charger 65W', slug='fast-wall-charger-65w', description='GaN charger with dual USB-C.', image=IMG['charger'], price=129, compare_at=179, stock=90, sold=55, rating=4.4, review_count=11, category_id=5, subcategory_id=12, brand_id=6),
            Product(name='20,000mAh Power Bank', slug='power-bank-20000', description='High-capacity power bank.', image=IMG['powerbank'], price=159, compare_at=199, stock=70, sold=88, rating=4.2, review_count=19, category_id=5, subcategory_id=13, brand_id=1),
            Product(name='DSLR Camera Kit', slug='dslr-camera-kit', description='24MP DSLR with 18-55mm lens.', image=IMG['camera'], price=2899, compare_at=3299, stock=9, sold=6, rating=4.5, review_count=5, is_featured=True, category_id=6, subcategory_id=14, brand_id=7),
            Product(name='Travel Tripod', slug='travel-tripod', description='Compact aluminum tripod.', image=IMG['tripod'], price=189, compare_at=249, stock=34, sold=17, rating=4.0, review_count=3, category_id=6, subcategory_id=15, brand_id=7),
            Product(name='55-inch 4K Smart TV', slug='55-inch-4k-smart-tv', description='4K HDR smart TV.', image=IMG['tv'], price=1899, compare_at=2299, stock=14, sold=22, rating=4.4, review_count=16, is_featured=True, category_id=7, subcategory_id=16, brand_id=1),
            Product(name='2.1 Home Theatre Soundbar', slug='home-theatre-soundbar', description='Soundbar plus wireless subwoofer.', image=IMG['theatre'], price=799, compare_at=999, stock=20, sold=13, rating=4.3, review_count=8, category_id=7, subcategory_id=17, brand_id=7),
            Product(name='Leather Crossbody Bag', slug='leather-crossbody-bag', description='Structured leather bag.', image=IMG['bag'], price=1299, compare_at=1599, stock=15, sold=7, rating=4.6, review_count=4, category_id=8, brand_id=4),
            Product(name='All-in-One Desktop', slug='all-in-one-desktop', description='27-inch all-in-one desktop.', image=IMG['desktop'], price=3999, compare_at=4499, stock=8, sold=3, rating=4.2, review_count=2, category_id=2, subcategory_id=5, brand_id=6),
        ])
        db.session.flush()
        db.session.add_all([
            Banner(title='Shoes Sale', image=IMG['banner1'], link='/shop?category=8', sort_order=1),
            Banner(title='Get 200 off on first Brand', image=IMG['banner2'], link='/shop?brand=1', sort_order=2),
            Banner(title='Seasonal Offers', image=IMG['banner3'], link='/shop', sort_order=3),
            Promo(title='Special Offer On Headphones', image=IMG['promo1'], link='/shop?category=4'),
            Promo(title='Special Offer On Products', image=IMG['promo2'], link='/shop?brand=7'),
        ])
        s23 = Product.query.filter_by(slug='samsung-galaxy-s23').first()
        ws = Product.query.filter_by(slug='white-sneakers').first()
        brs = Product.query.filter_by(slug='black-running-sneakers').first()
        db.session.add_all([
            Review(product=s23, user=demo, rating=3, comment='Good camera, battery is average.'),
            Review(product=s23, user=admin, rating=4, comment='Solid flagship.'),
            Review(product=ws, user=demo, rating=5, comment='Comfortable and look expensive.'),
            Review(product=brs, user=demo, rating=4, comment='Great for evening runs around the Corniche.'),
        ])
        db.session.commit()
