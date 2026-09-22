from datetime import datetime, timedelta

from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

_INSTALLED = False


def register_admin(app):
    global _INSTALLED
    if _INSTALLED or getattr(app, "_admin_panel", False):
        return
    app._admin_panel = True
    _INSTALLED = True
    from extensions import db
    from flash_sale import FlashSale
    from models import Banner, Category, Product, Promo, User

    def gate():
        if not getattr(current_user, "is_authenticated", False) or not getattr(current_user, "is_admin", False):
            abort(403)

    def _parse_dt(value):
        value = (value or "").strip()
        if not value:
            return None
        try:
            return datetime.fromisoformat(value)
        except Exception:
            return None

    def _apply_sale(sale, on):
        from flash_sale import apply_sale
        ok = apply_sale(sale, on)
        if on and not ok:
            flash("Select at least one product before starting the sale.", "info")
        return ok

    @app.route("/admin/sales")
    @login_required
    def admin_sales():
        gate()
        try:
            db.create_all()
            sales = FlashSale.query.order_by(FlashSale.id.desc()).all()
        except Exception:
            sales = []
        return render_template("admin_sales.html", sales=sales, products=Product.query.order_by(Product.name).all())

    @app.route("/admin/sales/create", methods=["POST"])
    @login_required
    def admin_sale_create():
        gate()
        ids = request.form.getlist("product_id")
        sale = FlashSale(
            title=(request.form.get("title") or "Flash sale")[:160],
            discount=float(request.form.get("discount") or 10),
            starts_at=_parse_dt(request.form.get("starts_at")),
            ends_at=_parse_dt(request.form.get("ends_at")),
            product_ids=",".join(ids),
            active=False,
        )
        db.session.add(sale)
        db.session.commit()
        flash("Campaign saved. Press Start now when you want it live.", "success")
        return redirect(url_for("admin_sales"))

    @app.route("/admin/sales/<int:sid>/start", methods=["POST"])
    @login_required
    def admin_sale_start(sid):
        gate()
        sale = db.session.get(FlashSale, sid) or abort(404)
        for other in FlashSale.query.filter(FlashSale.id != sid, FlashSale.active.is_(True)).all():
            _apply_sale(other, False)
        if _apply_sale(sale, True):
            flash("Flash sale is live. Only selected products are on deal.", "success")
        return redirect(url_for("admin_sales"))

    @app.route("/admin/sales/<int:sid>/stop", methods=["POST"])
    @login_required
    def admin_sale_stop(sid):
        gate()
        sale = db.session.get(FlashSale, sid) or abort(404)
        _apply_sale(sale, False)
        flash("Sale stopped.", "success")
        return redirect(url_for("admin_sales"))

    @app.route("/admin/sales/<int:sid>/delete", methods=["POST"])
    @login_required
    def admin_sale_delete(sid):
        gate()
        sale = db.session.get(FlashSale, sid) or abort(404)
        if sale.active:
            _apply_sale(sale, False)
        db.session.delete(sale)
        db.session.commit()
        flash("Campaign deleted.", "success")
        return redirect(url_for("admin_sales"))

    @app.route("/about")
    def about_alias():
        return redirect("/aboutus")

    @app.route("/contact")
    def contact_alias():
        return redirect("/contactus")

    @app.route("/categories")
    def categories_alias():
        return redirect("/shop")

    @app.route("/returns")
    def returns_alias():
        return redirect("/return-policy")

    @app.route("/admin/products", methods=["GET", "POST"])
    @login_required
    def admin_products():
        gate()
        if request.method == "POST":
            name = (request.form.get("name") or "").strip()
            if name:
                slug = name.lower().replace(" ", "-")[:200]
                db.session.add(Product(name=name, slug=slug, description=request.form.get("description") or "", image=request.form.get("image") or "", price=float(request.form.get("price") or 0), stock=int(request.form.get("stock") or 0), category_id=int(request.form.get("category_id") or 0) or None, is_flash=bool(request.form.get("is_flash"))))
                db.session.commit()
                flash("Product added.", "success")
            return redirect(url_for("admin_products"))
        return render_template("admin_products.html", products=Product.query.order_by(Product.id.desc()).all(), categories=Category.query.order_by(Category.name).all())

    @app.route("/admin/products/<int:pid>", methods=["POST"])
    @login_required
    def admin_product_save(pid):
        gate()
        p = db.session.get(Product, pid) or abort(404)
        if request.form.get("delete"):
            db.session.delete(p)
            db.session.commit()
            flash("Product removed.", "success")
            return redirect(url_for("admin_products"))
        p.name = request.form.get("name") or p.name
        p.price = float(request.form.get("price") or p.price)
        p.stock = int(request.form.get("stock") or p.stock or 0)
        p.is_flash = bool(request.form.get("is_flash"))
        db.session.commit()
        flash("Product updated.", "success")
        return redirect(url_for("admin_products"))

    @app.route("/admin/users")
    @login_required
    def admin_users():
        gate()
        return render_template("admin_users.html", users=User.query.order_by(User.id).all())

    @app.route("/admin/users/<int:uid>", methods=["POST"])
    @login_required
    def admin_user_save(uid):
        gate()
        u = db.session.get(User, uid) or abort(404)
        if request.form.get("delete") and u.id != current_user.id:
            db.session.delete(u)
            db.session.commit()
            flash("User removed.", "success")
            return redirect(url_for("admin_users"))
        u.name = request.form.get("name") or u.name
        u.is_admin = bool(request.form.get("is_admin"))
        if request.form.get("password"):
            u.set_password(request.form.get("password"))
        db.session.commit()
        flash("User updated.", "success")
        return redirect(url_for("admin_users"))

    @app.route("/admin/banners", methods=["GET", "POST"])
    @login_required
    def admin_banners():
        gate()
        if request.method == "POST":
            title = request.form.get("title") or ""
            image = request.form.get("image") or ""
            link = request.form.get("link") or "/shop"
            if request.form.get("kind") == "promo":
                db.session.add(Promo(title=title, image=image, link=link))
            else:
                db.session.add(Banner(title=title, image=image, link=link, sort_order=int(request.form.get("sort_order") or 0)))
            db.session.commit()
            flash("Banner saved.", "success")
            return redirect(url_for("admin_banners"))
        return render_template("admin_banners.html", banners=Banner.query.order_by(Banner.sort_order, Banner.id).all(), promos=Promo.query.all())

    @app.route("/admin/banners/<kind>/<int:bid>", methods=["POST"])
    @login_required
    def admin_banner_save(kind, bid):
        gate()
        row = db.session.get(Promo if kind == "promo" else Banner, bid) or abort(404)
        if request.form.get("delete"):
            db.session.delete(row)
            db.session.commit()
            flash("Removed.", "success")
            return redirect(url_for("admin_banners"))
        row.title = request.form.get("title") or row.title
        row.image = request.form.get("image") or row.image
        row.link = request.form.get("link") or row.link
        db.session.commit()
        flash("Updated.", "success")
        return redirect(url_for("admin_banners"))

    @app.route("/admin/settings")
    @login_required
    def admin_settings():
        gate()
        return render_template("admin_settings.html")
