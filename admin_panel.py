from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

_INSTALLED = False

def register_admin(app):
    global _INSTALLED
    if _INSTALLED or getattr(app, '_admin_panel', False):
        return
    app._admin_panel = True
    _INSTALLED = True
    from extensions import db
    from models import User, Product, Category, Banner, Promo

    def gate():
        if not getattr(current_user, 'is_authenticated', False) or not getattr(current_user, 'is_admin', False):
            abort(403)

    @app.route('/about')
    def about_alias():
        return redirect('/aboutus')

    @app.route('/contact')
    def contact_alias():
        return redirect('/contactus')

    @app.route('/categories')
    def categories_alias():
        return redirect('/shop/category/index')

    @app.route('/returns')
    def returns_alias():
        return redirect('/return-policy')

    @app.route('/cookies')
    def cookies_alias():
        return redirect('/cookie-policy')

    @app.route('/shipping-policy')
    def shipping_alias():
        return redirect('/site/shipping-policy')

    @app.route('/admin/products', methods=['GET', 'POST'])
    @login_required
    def admin_products():
        gate()
        if request.method == 'POST':
            name = (request.form.get('name') or '').strip()
            if name:
                slug = name.lower().replace(' ', '-')[:200]
                db.session.add(Product(name=name, slug=slug, description=request.form.get('description') or '', image=request.form.get('image') or '', price=float(request.form.get('price') or 0), compare_at=float(request.form.get('compare_at') or 0) or None, stock=int(request.form.get('stock') or 0), category_id=int(request.form.get('category_id') or 0) or None, is_featured=bool(request.form.get('is_featured')), is_flash=bool(request.form.get('is_flash')), is_bestseller=bool(request.form.get('is_bestseller'))))
                db.session.commit()
                flash('Product added.', 'success')
            return redirect(url_for('admin_products'))
        return render_template('admin_products.html', products=Product.query.order_by(Product.id.desc()).all(), categories=Category.query.order_by(Category.name).all())

    @app.route('/admin/products/<int:pid>', methods=['POST'])
    @login_required
    def admin_product_save(pid):
        gate()
        p = db.session.get(Product, pid) or abort(404)
        if request.form.get('delete'):
            db.session.delete(p); db.session.commit(); flash('Product deleted.', 'success')
            return redirect(url_for('admin_products'))
        p.name = request.form.get('name') or p.name
        p.price = float(request.form.get('price') or p.price or 0)
        p.stock = int(request.form.get('stock') or p.stock or 0)
        p.image = request.form.get('image') or p.image
        p.is_featured = bool(request.form.get('is_featured'))
        p.is_flash = bool(request.form.get('is_flash'))
        p.is_bestseller = bool(request.form.get('is_bestseller'))
        db.session.commit(); flash('Product updated.', 'success')
        return redirect(url_for('admin_products'))

    @app.route('/admin/users', methods=['GET', 'POST'])
    @login_required
    def admin_users():
        gate()
        if request.method == 'POST':
            email = (request.form.get('email') or '').strip().lower()
            if email and not User.query.filter_by(email=email).first():
                u = User(name=request.form.get('name') or email.split('@')[0], email=email, is_admin=bool(request.form.get('is_admin')))
                u.set_password(request.form.get('password') or 'changeme123')
                db.session.add(u); db.session.commit(); flash('User created.', 'success')
            return redirect(url_for('admin_users'))
        return render_template('admin_users.html', users=User.query.order_by(User.id).all())

    @app.route('/admin/users/<int:uid>', methods=['POST'])
    @login_required
    def admin_user_save(uid):
        gate()
        u = db.session.get(User, uid) or abort(404)
        if request.form.get('delete') and u.id != current_user.id:
            db.session.delete(u); db.session.commit(); flash('User removed.', 'success')
            return redirect(url_for('admin_users'))
        u.name = request.form.get('name') or u.name
        u.is_admin = bool(request.form.get('is_admin'))
        if request.form.get('password'):
            u.set_password(request.form.get('password'))
        db.session.commit(); flash('User updated.', 'success')
        return redirect(url_for('admin_users'))

    @app.route('/admin/banners', methods=['GET', 'POST'])
    @login_required
    def admin_banners():
        gate()
        if request.method == 'POST':
            title = request.form.get('title') or ''
            image = request.form.get('image') or ''
            link = request.form.get('link') or '/shop'
            if request.form.get('kind') == 'promo':
                db.session.add(Promo(title=title, image=image, link=link))
            else:
                db.session.add(Banner(title=title, image=image, link=link, sort_order=int(request.form.get('sort_order') or 0)))
            db.session.commit(); flash('Banner saved.', 'success')
            return redirect(url_for('admin_banners'))
        return render_template('admin_banners.html', banners=Banner.query.order_by(Banner.sort_order, Banner.id).all(), promos=Promo.query.all())

    @app.route('/admin/banners/<kind>/<int:bid>', methods=['POST'])
    @login_required
    def admin_banner_save(kind, bid):
        gate()
        row = db.session.get(Promo if kind == 'promo' else Banner, bid) or abort(404)
        if request.form.get('delete'):
            db.session.delete(row); db.session.commit(); flash('Removed.', 'success')
            return redirect(url_for('admin_banners'))
        row.title = request.form.get('title') or row.title
        row.image = request.form.get('image') or row.image
        row.link = request.form.get('link') or row.link
        if kind != 'promo':
            row.sort_order = int(request.form.get('sort_order') or 0)
        db.session.commit(); flash('Updated.', 'success')
        return redirect(url_for('admin_banners'))

    @app.route('/admin/settings')
    @login_required
    def admin_settings():
        gate()
        return render_template('admin_settings.html')
