import os
import secrets
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_, func

from config import Config
from extensions import db, login_manager
from models import User, Category, SubCategory, Brand, Product, CartItem, WishlistItem, Order, OrderItem, Review, Banner, Promo, Address
from seed import seed_all

ROOT = Path(__file__).resolve().parent

def create_app():
    on_vercel = bool(os.environ.get('VERCEL') or os.environ.get('VERCEL_ENV'))
    app = Flask(
        __name__,
        instance_path='/tmp' if on_vercel else str(ROOT / 'instance'),
        template_folder=str(ROOT / 'templates'),
        static_folder=str(ROOT / 'static'),
    )
    app.config.from_object(Config)
    try:
        Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        try:
            db.create_all()
            seed_all(app)
        except Exception as exc:
            app.logger.exception('db bootstrap failed: %s', exc)

    @app.context_processor
    def inject_globals():
        try:
            cats = Category.query.order_by(Category.id).all()
            brands = Brand.query.order_by(Brand.name).all()
        except Exception:
            cats, brands = [], []
        cart_count = wish_count = cart_total = 0
        wish_ids = []
        try:
            if current_user.is_authenticated:
                items = CartItem.query.filter_by(user_id=current_user.id).all()
                cart_count = sum(i.quantity for i in items)
                cart_total = sum(i.quantity * i.product.price for i in items if i.product)
                wish_count = WishlistItem.query.filter_by(user_id=current_user.id).count()
                wish_ids = [i.product_id for i in WishlistItem.query.filter_by(user_id=current_user.id).all()]
            else:
                guest = session.get('cart', {})
                cart_count = sum(guest.values())
                if guest:
                    products = Product.query.filter(Product.id.in_(list(map(int, guest.keys())))).all()
                    cart_total = sum(p.price * guest.get(str(p.id), 0) for p in products)
                wish_count = len(session.get('wishlist', []))
                wish_ids = list(session.get('wishlist', []))
        except Exception:
            pass
        return {
            'store_name': app.config.get('STORE_NAME', '11-11'), 'currency': app.config.get('CURRENCY', 'QAR'),
            'all_categories': cats, 'all_brands': brands, 'nav_cart_count': cart_count,
            'nav_wish_count': wish_count, 'nav_cart_total': cart_total,
            'flash_sale_end': app.config.get('FLASH_SALE_END', ''), 'year': datetime.utcnow().year,
            'wishlist_ids': wish_ids, 'lang': session.get('lang', 'en'),
            'deliver_to': session.get('deliver_to', 'Detecting...'),
            'qatar_areas': ['Doha — West Bay', 'Doha — The Pearl', 'Doha — Lusail', 'Doha — Al Sadd', 'Al Wakrah', 'Al Khor', 'Al Rayyan'],
        }

    def money(value):
        try:
            value = float(value)
        except (TypeError, ValueError):
            return 'QAR 0'
        return f'QAR {value:,.0f}' if value >= 1000 else f'QAR {value:,.2f}'.rstrip('0').rstrip('.')
    app.jinja_env.filters['qar'] = money

    def merge_guest_cart(user):
        for pid, qty in session.pop('cart', {}).items():
            item = CartItem.query.filter_by(user_id=user.id, product_id=int(pid)).first()
            if item:
                item.quantity += int(qty)
            else:
                db.session.add(CartItem(user_id=user.id, product_id=int(pid), quantity=int(qty)))
        for pid in session.pop('wishlist', []):
            if not WishlistItem.query.filter_by(user_id=user.id, product_id=int(pid)).first():
                db.session.add(WishlistItem(user_id=user.id, product_id=int(pid)))
        db.session.commit()

    def get_cart_rows():
        rows = []
        if current_user.is_authenticated:
            for it in CartItem.query.filter_by(user_id=current_user.id).all():
                if it.product:
                    rows.append({'product': it.product, 'qty': it.quantity, 'line': it.product.price * it.quantity})
        else:
            guest = session.get('cart', {})
            if guest:
                products = {p.id: p for p in Product.query.filter(Product.id.in_(list(map(int, guest.keys())))).all()}
                for pid, qty in guest.items():
                    p = products.get(int(pid))
                    if p:
                        rows.append({'product': p, 'qty': qty, 'line': p.price * qty})
        return rows

    def wishlist_ids():
        if current_user.is_authenticated:
            return [i.product_id for i in WishlistItem.query.filter_by(user_id=current_user.id).all()]
        return list(session.get('wishlist', []))

    def cart_payload():
        rows = get_cart_rows()
        subtotal = sum(r['line'] for r in rows)
        shipping = 0 if subtotal >= 200 or subtotal == 0 else 25
        coupon = session.get('coupon')
        discount = round(subtotal * 0.10, 2) if coupon == 'FLASH10' else 0
        items = [{'id': r['product'].id, 'name': r['product'].name, 'slug': r['product'].slug, 'image': r['product'].image, 'price': r['product'].price, 'qty': r['qty'], 'line': r['line'], 'stock': r['product'].stock} for r in rows]
        return {'ok': True, 'count': sum(r['qty'] for r in rows), 'wish_count': len(wishlist_ids()), 'wishlist_ids': wishlist_ids(), 'subtotal': subtotal, 'shipping': shipping, 'discount': discount, 'coupon': coupon, 'total': max(0, subtotal + shipping - discount), 'items': items, 'currency': 'QAR'}

    def add_to_cart(pid, qty=1):
        product = db.session.get(Product, pid)
        if not product:
            return None
        qty = max(1, min(int(qty or 1), product.stock or 1))
        if current_user.is_authenticated:
            item = CartItem.query.filter_by(user_id=current_user.id, product_id=pid).first()
            if item:
                item.quantity = min(item.quantity + qty, product.stock)
            else:
                db.session.add(CartItem(user_id=current_user.id, product_id=pid, quantity=qty))
            db.session.commit()
        else:
            cart = session.get('cart', {})
            cart[str(pid)] = min(cart.get(str(pid), 0) + qty, product.stock)
            session['cart'] = cart
        return product

    def set_cart_qty(pid, qty):
        product = db.session.get(Product, pid)
        qty = max(0, int(qty or 0))
        if product:
            qty = min(qty, product.stock)
        if qty <= 0:
            if current_user.is_authenticated:
                CartItem.query.filter_by(user_id=current_user.id, product_id=pid).delete()
                db.session.commit()
            else:
                cart = session.get('cart', {})
                cart.pop(str(pid), None)
                session['cart'] = cart
            return
        if current_user.is_authenticated:
            item = CartItem.query.filter_by(user_id=current_user.id, product_id=pid).first()
            if item:
                item.quantity = qty
            else:
                db.session.add(CartItem(user_id=current_user.id, product_id=pid, quantity=qty))
            db.session.commit()
        else:
            cart = session.get('cart', {})
            cart[str(pid)] = qty
            session['cart'] = cart

    def toggle_wish(pid):
        added = False
        if current_user.is_authenticated:
            exists = WishlistItem.query.filter_by(user_id=current_user.id, product_id=pid).first()
            if exists:
                db.session.delete(exists)
            else:
                db.session.add(WishlistItem(user_id=current_user.id, product_id=pid))
                added = True
            db.session.commit()
        else:
            w = list(session.get('wishlist', []))
            if pid in w:
                w.remove(pid)
            else:
                w.append(pid)
                added = True
            session['wishlist'] = w
        return added

    @app.route('/')
    def index():
        return render_template('index.html', banners=Banner.query.order_by(Banner.sort_order).all(), promos=Promo.query.all(), flash_products=Product.query.filter_by(is_flash=True).limit(3).all(), bestsellers=Product.query.filter_by(is_bestseller=True).order_by(Product.sold.desc()).limit(6).all(), recommended=Product.query.order_by(Product.is_featured.desc(), Product.sold.desc()).limit(8).all(), accessory_deals=Product.query.filter_by(category_id=5).limit(8).all())

    @app.route('/shop')
    @app.route('/shop/product/index')
    def shop():
        q = request.args.get('q', '').strip()
        category_id = request.args.get('category') or request.args.get('category_id')
        sub_id = request.args.get('sub_category_id')
        brand_id = request.args.get('brand') or request.args.get('brand_id')
        sort = request.args.get('sort', 'featured')
        page = request.args.get('page', 1, type=int)
        query = Product.query
        active_cat = active_sub = active_brand = None
        if category_id:
            query = query.filter_by(category_id=int(category_id))
            active_cat = db.session.get(Category, int(category_id))
        if sub_id:
            query = query.filter_by(subcategory_id=int(sub_id))
            active_sub = db.session.get(SubCategory, int(sub_id))
        if brand_id:
            query = query.filter_by(brand_id=int(brand_id))
            active_brand = db.session.get(Brand, int(brand_id))
        if q:
            like = f'%{q}%'
            query = query.filter(or_(Product.name.ilike(like), Product.description.ilike(like)))
        if sort == 'price_asc':
            query = query.order_by(Product.price.asc())
        elif sort == 'price_desc':
            query = query.order_by(Product.price.desc())
        elif sort == 'newest':
            query = query.order_by(Product.created_at.desc())
        else:
            query = query.order_by(Product.is_featured.desc(), Product.sold.desc())
        pagination = query.paginate(page=page, per_page=app.config['ITEMS_PER_PAGE'], error_out=False)
        return render_template('shop.html', products=pagination.items, pagination=pagination, q=q, sort=sort, active_cat=active_cat, active_sub=active_sub, active_brand=active_brand)

    @app.route('/shop/product/search')
    def search():
        return redirect(url_for('shop', q=request.args.get('q', '')))
    @app.route('/shop/category/index')
    def categories_page():
        return render_template('categories.html')
    @app.route('/product/<int:pid>/<slug>')
    @app.route('/shop/product/<int:pid>/<slug>')
    def product_detail(pid, slug):
        product = db.session.get(Product, pid) or abort(404)
        related = Product.query.filter(Product.category_id == product.category_id, Product.id != product.id).limit(4).all()
        reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
        return render_template('product.html', product=product, related=related, reviews=reviews)
    @app.route('/cart/add/<int:pid>', methods=['POST', 'GET'])
    def cart_add(pid):
        product = add_to_cart(pid, request.form.get('qty', 1, type=int) or 1)
        if not product:
            abort(404)
        if request.headers.get('X-Requested-With') == 'fetch' or request.is_json:
            data = cart_payload(); data['message'] = f'{product.name} added to cart.'; return jsonify(data)
        flash(f'{product.name} added to cart.', 'success')
        return redirect(request.referrer or url_for('cart'))
    @app.route('/api/cart')
    def api_cart():
        return jsonify(cart_payload())
    @app.route('/api/cart/add', methods=['POST'])
    def api_cart_add():
        data = request.get_json(silent=True) or request.form
        product = add_to_cart(int(data.get('pid') or data.get('id') or 0), int(data.get('qty') or 1))
        if not product:
            return jsonify({'ok': False, 'error': 'Product not found'}), 404
        payload = cart_payload(); payload['message'] = f'{product.name} added to cart.'; return jsonify(payload)
    @app.route('/api/cart/update', methods=['POST'])
    def api_cart_update():
        data = request.get_json(silent=True) or request.form
        set_cart_qty(int(data.get('pid') or 0), int(data.get('qty') or 1))
        return jsonify(cart_payload())
    @app.route('/api/cart/remove', methods=['POST'])
    def api_cart_remove():
        data = request.get_json(silent=True) or request.form
        set_cart_qty(int(data.get('pid') or 0), 0)
        payload = cart_payload(); payload['message'] = 'Item removed.'; return jsonify(payload)
    @app.route('/api/wishlist/toggle', methods=['POST'])
    def api_wishlist_toggle():
        data = request.get_json(silent=True) or request.form
        pid = int(data.get('pid') or data.get('id') or 0)
        if not db.session.get(Product, pid):
            return jsonify({'ok': False}), 404
        added = toggle_wish(pid)
        payload = cart_payload(); payload['added'] = added; payload['message'] = 'Saved to wishlist.' if added else 'Removed from wishlist.'; return jsonify(payload)
    @app.route('/api/search')
    def api_search():
        q = (request.args.get('q') or '').strip()
        if len(q) < 2:
            return jsonify({'results': []})
        like = f'%{q}%'
        items = Product.query.filter(or_(Product.name.ilike(like), Product.description.ilike(like))).limit(8).all()
        return jsonify({'results': [{'id': p.id, 'name': p.name, 'slug': p.slug, 'image': p.image, 'price': p.price, 'url': url_for('product_detail', pid=p.id, slug=p.slug)} for p in items]})
    @app.route('/api/coupon', methods=['POST'])
    def api_coupon():
        data = request.get_json(silent=True) or request.form
        code = (data.get('code') or '').strip().upper()
        if code == 'FLASH10':
            session['coupon'] = code
            payload = cart_payload(); payload['message'] = 'Coupon FLASH10 applied (10% off).'; return jsonify(payload)
        session.pop('coupon', None)
        payload = cart_payload(); payload['ok'] = False; payload['message'] = 'Invalid coupon. Try FLASH10.'; return jsonify(payload)
    @app.route('/api/location', methods=['POST'])
    def api_location():
        data = request.get_json(silent=True) or request.form
        session['deliver_to'] = (data.get('area') or '').strip() or 'Doha'
        return jsonify({'ok': True, 'area': session['deliver_to']})
    @app.route('/lang/<code>')
    def set_lang(code):
        session['lang'] = 'ar' if code == 'ar' else 'en'
        return redirect(request.referrer or url_for('index'))
    @app.route('/cart')
    @app.route('/shop/cart')
    def cart():
        rows = get_cart_rows()
        subtotal = sum(r['line'] for r in rows)
        shipping = 0 if subtotal >= 200 or subtotal == 0 else 25
        discount = round(subtotal * 0.10, 2) if session.get('coupon') == 'FLASH10' else 0
        return render_template('cart.html', rows=rows, subtotal=subtotal, shipping=shipping, discount=discount, coupon=session.get('coupon'), total=max(0, subtotal + shipping - discount))
    @app.route('/checkout', methods=['GET', 'POST'])
    @app.route('/shop/cart/checkout', methods=['GET', 'POST'])
    def checkout():
        rows = get_cart_rows()
        if not rows:
            flash('Your cart is empty.', 'info'); return redirect(url_for('shop'))
        subtotal = sum(r['line'] for r in rows)
        shipping = 0 if subtotal >= 200 else 25
        discount = round(subtotal * 0.10, 2) if session.get('coupon') == 'FLASH10' else 0
        total = max(0, subtotal + shipping - discount)
        if request.method == 'POST':
            if not current_user.is_authenticated:
                flash('Please log in or create an account to place an order.', 'info')
                return redirect(url_for('login', next=url_for('checkout')))
            name = request.form.get('name', '').strip(); phone = request.form.get('phone', '').strip(); address = request.form.get('address', '').strip(); city = request.form.get('city', 'Doha').strip(); method = request.form.get('payment_method', 'cod')
            if not name or not phone or not address:
                flash('Please fill name, phone and address.', 'danger')
                return render_template('checkout.html', rows=rows, subtotal=subtotal, shipping=shipping, discount=discount, coupon=session.get('coupon'), total=total)
            order_no = '1111-' + secrets.token_hex(4).upper()
            order = Order(user_id=current_user.id, order_number=order_no, status='confirmed' if method == 'cod' else 'pending', payment_method=method, subtotal=subtotal, shipping=shipping, total=total, shipping_name=name, shipping_phone=phone, shipping_address=address, shipping_city=city, note=request.form.get('note', ''))
            db.session.add(order); db.session.flush()
            for r in rows:
                p = r['product']
                db.session.add(OrderItem(order_id=order.id, product_id=p.id, name=p.name, price=p.price, quantity=r['qty'], image=p.image))
                p.sold += r['qty']; p.stock = max(0, p.stock - r['qty'])
            CartItem.query.filter_by(user_id=current_user.id).delete(); db.session.commit()
            flash(f'Order {order_no} placed successfully.', 'success')
            return redirect(url_for('order_thanks', order_number=order_no))
        return render_template('checkout.html', rows=rows, subtotal=subtotal, shipping=shipping, discount=discount, coupon=session.get('coupon'), total=total)
    @app.route('/order/thanks/<order_number>')
    @login_required
    def order_thanks(order_number):
        return render_template('thanks.html', order=Order.query.filter_by(order_number=order_number, user_id=current_user.id).first_or_404())
    @app.route('/account/orders')
    @login_required
    def my_orders():
        return render_template('orders.html', orders=Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all())
    @app.route('/shop/order/track', methods=['GET', 'POST'])
    @app.route('/track', methods=['GET', 'POST'])
    def track_order():
        order = None
        if request.method == 'POST' or request.args.get('n'):
            n = request.form.get('order_number') or request.args.get('n')
            if n:
                order = Order.query.filter_by(order_number=n.strip()).first()
                if not order:
                    flash('No order found with that number.', 'danger')
        return render_template('track.html', order=order)
    @app.route('/wishlist/add/<int:pid>')
    @app.route('/shop/wishlist/add-wishlist')
    def wishlist_add(pid=None):
        pid = pid or request.args.get('id', type=int)
        if pid:
            toggle_wish(pid); flash('Saved to wishlist.', 'success')
        return redirect(request.referrer or url_for('wishlist'))
    @app.route('/wishlist/remove/<int:pid>')
    def wishlist_remove(pid):
        if current_user.is_authenticated:
            WishlistItem.query.filter_by(user_id=current_user.id, product_id=pid).delete(); db.session.commit()
        else:
            session['wishlist'] = [x for x in session.get('wishlist', []) if x != pid]
        return redirect(url_for('wishlist'))
    @app.route('/wishlist')
    @app.route('/shop/wishlist')
    def wishlist():
        products = []
        if current_user.is_authenticated:
            products = [i.product for i in WishlistItem.query.filter_by(user_id=current_user.id).all() if i.product]
        else:
            ids = session.get('wishlist', [])
            if ids:
                products = Product.query.filter(Product.id.in_(ids)).all()
        return render_template('wishlist.html', products=products)
    @app.route('/login', methods=['GET', 'POST'])
    @app.route('/user/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form.get('email', '').strip().lower()).first()
            if user and user.check_password(request.form.get('password', '')):
                login_user(user, remember=True); merge_guest_cart(user)
                flash(f'Welcome back, {user.name}.', 'success')
                return redirect(request.args.get('next') or url_for('index'))
            flash('Invalid email or password.', 'danger')
        return render_template('login.html')
    @app.route('/register', methods=['GET', 'POST'])
    @app.route('/user/signup', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('name', '').strip(); email = request.form.get('email', '').strip().lower(); password = request.form.get('password', '')
            if not name or not email or len(password) < 6:
                flash('Name, email and a password of at least 6 characters are required.', 'danger')
            elif User.query.filter_by(email=email).first():
                flash('That email is already registered.', 'danger')
            else:
                user = User(name=name, email=email, phone=request.form.get('phone')); user.set_password(password)
                db.session.add(user); db.session.commit(); login_user(user); merge_guest_cart(user)
                flash('Account created.', 'success'); return redirect(url_for('index'))
        return render_template('register.html')
    @app.route('/logout')
    def logout():
        logout_user(); flash('Signed out.', 'info'); return redirect(url_for('index'))
    @app.route('/account', methods=['GET', 'POST'])
    @login_required
    def account():
        if request.method == 'POST':
            current_user.name = request.form.get('name', current_user.name)
            current_user.phone = request.form.get('phone', current_user.phone)
            db.session.commit(); flash('Profile updated.', 'success')
        return render_template('account.html')
    @app.route('/user/signup-vendor', methods=['GET', 'POST'])
    def become_seller():
        if request.method == 'POST':
            flash('Seller application received. We will contact you shortly.', 'success'); return redirect(url_for('index'))
        return render_template('seller.html')
    @app.route('/product/<int:pid>/review', methods=['POST'])
    @login_required
    def add_review(pid):
        product = db.session.get(Product, pid) or abort(404)
        rating = max(1, min(5, request.form.get('rating', 5, type=int))); comment = request.form.get('comment', '').strip()
        existing = Review.query.filter_by(product_id=pid, user_id=current_user.id).first()
        if existing:
            existing.rating = rating; existing.comment = comment
        else:
            db.session.add(Review(product_id=pid, user_id=current_user.id, rating=rating, comment=comment))
        db.session.flush()
        agg = db.session.query(func.avg(Review.rating), func.count(Review.id)).filter_by(product_id=pid).first()
        product.rating = round(float(agg[0] or 0), 1); product.review_count = int(agg[1] or 0)
        db.session.commit(); flash('Thanks for the review.', 'success')
        return redirect(url_for('product_detail', pid=product.id, slug=product.slug))
    @app.route('/aboutus')
    def about():
        return render_template('page.html', title='Our Story', body='about')
    @app.route('/contactus', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            flash('Message sent. Our team will reply by email.', 'success'); return redirect(url_for('contact'))
        return render_template('contact.html')
    @app.route('/faq')
    def faq():
        return render_template('faq.html')
    @app.route('/privacy')
    def privacy():
        return render_template('page.html', title='Privacy Policy', body='privacy')
    @app.route('/terms')
    def terms():
        return render_template('page.html', title='Terms of Service', body='terms')
    @app.route('/cookie-policy')
    def cookies():
        return render_template('page.html', title='Cookie Policy', body='cookies')
    @app.route('/accessibility')
    def accessibility():
        return render_template('page.html', title='Accessibility', body='access')
    @app.route('/return-policy')
    def returns():
        return render_template('page.html', title='Returns', body='returns')
    @app.route('/site/shipping-policy')
    def shipping_policy():
        return render_template('page.html', title='Shipping Info', body='shipping')
    @app.route('/blog')
    def blog():
        return render_template('page.html', title='Blog', body='blog')
    def admin_required():
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
    @app.route('/admin')
    @login_required
    def admin_home():
        admin_required()
        stats = {'products': Product.query.count(), 'orders': Order.query.count(), 'users': User.query.count(), 'revenue': db.session.query(func.coalesce(func.sum(Order.total), 0)).scalar()}
        return render_template('admin.html', stats=stats, orders=Order.query.order_by(Order.created_at.desc()).limit(12).all(), products=Product.query.order_by(Product.id).all())
    @app.route('/admin/product/<int:pid>', methods=['POST'])
    @login_required
    def admin_update_product(pid):
        admin_required(); p = db.session.get(Product, pid) or abort(404)
        p.price = float(request.form.get('price', p.price)); p.stock = int(request.form.get('stock', p.stock)); p.name = request.form.get('name', p.name)
        db.session.commit(); flash('Product updated.', 'success'); return redirect(url_for('admin_home'))
    @app.route('/admin/order/<int:oid>/status', methods=['POST'])
    @login_required
    def admin_order_status(oid):
        admin_required(); order = db.session.get(Order, oid) or abort(404)
        order.status = request.form.get('status', order.status); db.session.commit(); flash('Order status updated.', 'success'); return redirect(url_for('admin_home'))
    @app.errorhandler(404)
    def not_found(_e):
        return render_template('page.html', title='Page not found', body='404'), 404
    @app.errorhandler(403)
    def forbidden(_e):
        return render_template('page.html', title='Access denied', body='403'), 403
    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=int(os.environ.get('PORT', 5000)), debug=os.environ.get('FLASK_DEBUG', '1') == '1')
