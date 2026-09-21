from flask import session

STRINGS = {
    "deliver_to": {"en": "Deliver to", "ar": "التوصيل إلى"},
    "search": {"en": "Search 11-11", "ar": "ابحث في 11-11"},
    "wishlist": {"en": "Wishlist", "ar": "المفضلة"},
    "cart": {"en": "Cart", "ar": "السلة"},
    "login": {"en": "Login", "ar": "تسجيل الدخول"},
    "view_cart": {"en": "View Cart", "ar": "عرض السلة"},
    "checkout": {"en": "Checkout", "ar": "إتمام الطلب"},
    "about": {"en": "About Us", "ar": "من نحن"},
    "service": {"en": "Help", "ar": "المساعدة"},
    "categories": {"en": "Categories", "ar": "الأقسام"},
    "legal": {"en": "Legal", "ar": "قانوني"},
    "shop_by_category": {"en": "Shop by category", "ar": "تسوق حسب القسم"},
    "deals": {"en": "Deals of the day", "ar": "عروض اليوم"},
    "view_all": {"en": "View all", "ar": "عرض الكل"},
    "add_to_cart": {"en": "Add to cart", "ar": "أضف للسلة"},
    "shop_now": {"en": "Shop now", "ar": "تسوق الآن"},
    "hero_title": {"en": "Up to 50% off selected items", "ar": "خصم حتى 50% على منتجات مختارة"},
    "hero_text": {"en": "Electronics, fashion and home delivered in Qatar.", "ar": "إلكترونيات وأزياء ومنزل — التوصيل في قطر."},
    "privacy": {"en": "Privacy", "ar": "الخصوصية"},
    "shop": {"en": "Shop", "ar": "المتجر"},
    "empty_cart": {"en": "Your cart is empty.", "ar": "سلتك فارغة."},
    "continue": {"en": "Continue shopping", "ar": "واصل التسوق"},
    "summary": {"en": "Summary", "ar": "الملخص"},
    "subtotal": {"en": "Subtotal", "ar": "المجموع"},
    "shipping": {"en": "Shipping", "ar": "الشحن"},
    "discount": {"en": "Discount", "ar": "الخصم"},
    "total": {"en": "Total", "ar": "الإجمالي"},
    "delivery": {"en": "Delivery", "ar": "التوصيل"},
    "payment": {"en": "Payment method", "ar": "طريقة الدفع"},
    "cod": {"en": "Cash on delivery", "ar": "الدفع عند الاستلام"},
    "welcome": {"en": "Welcome back", "ar": "أهلاً بعودتك"},
    "orders": {"en": "Orders", "ar": "الطلبات"},
    "profile": {"en": "Profile", "ar": "الحساب"},
    "sign_in": {"en": "Sign in", "ar": "دخول"},
    "create": {"en": "Create account", "ar": "إنشاء حساب"},
    "price": {"en": "Price", "ar": "السعر"},
    "qty": {"en": "Qty", "ar": "الكمية"},
    "product": {"en": "Product", "ar": "المنتج"},
    "remove": {"en": "Remove", "ar": "حذف"},
    "contact": {"en": "Contact", "ar": "اتصل بنا"},
    "faq": {"en": "FAQ", "ar": "الأسئلة"},
    "terms": {"en": "Terms", "ar": "الشروط"},
    "returns": {"en": "Returns", "ar": "الإرجاع"},
    "track": {"en": "Track order", "ar": "تتبع الطلب"},
}

NAMES = {
    "Computer & Laptop": "الكمبيوتر واللابتوب",
    "SmartPhone": "الهواتف",
    "Headphones": "سماعات الرأس",
    "Accessories": "الإكسسوارات",
    "Camera & Photo": "الكاميرا والتصوير",
    "TV & Homes": "التلفاز والمنزل",
    "Fashion": "الأزياء",
}

AREAS = {
    "en": ["Doha — West Bay", "Doha — The Pearl", "Doha — Lusail", "Al Wakrah", "Al Khor"],
    "ar": ["الدوحة — الخليج الغربي", "الدوحة — اللؤلؤة", "الدوحة — لوسيل", "الوكر", "الخور"],
}


def translate(key, lang="en"):
    row = STRINGS.get(key) or {}
    return row.get(lang) or row.get("en") or key


def local_name(name, lang="en"):
    if lang == "ar":
        return NAMES.get(name, name)
    return name


def install_i18n(app):
    @app.context_processor
    def inject_i18n():
        lang = session.get("lang", "en")
        return {
            "t": lambda key: translate(key, lang),
            "is_rtl": lang == "ar",
            "qatar_areas": AREAS["ar"] if lang == "ar" else AREAS["en"],
        }

    @app.template_filter("arname")
    def arname(name):
        return local_name(name, session.get("lang", "en"))
