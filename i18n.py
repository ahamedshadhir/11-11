from flask import session

STRINGS = {
    "deliver_to": {"en": "Deliver to", "ar": "التوصيل إلى"},
    "search": {"en": "Search 11-11", "ar": "ابحث في 11-11"},
    "all_categories": {"en": "All Categories", "ar": "كل الأقسام"},
    "wishlist": {"en": "Wishlist", "ar": "المفضلة"},
    "cart": {"en": "Cart", "ar": "السلة"},
    "login": {"en": "Login", "ar": "تسجيل الدخول"},
    "admin": {"en": "Admin", "ar": "الإدارة"},
    "english": {"en": "English", "ar": "English"},
    "arabic": {"en": "العربية", "ar": "العربية"},
    "cookies": {"en": "We use cookies, check our", "ar": "نستخدم الكوكيز, راجع"},
    "privacy": {"en": "Privacy Policies", "ar": "سياسة الخصوصية"},
    "agree": {"en": "Agree", "ar": "موافق"},
    "menu": {"en": "Menu", "ar": "القائمة"},
    "view_cart": {"en": "View Cart", "ar": "عرض السلة"},
    "checkout": {"en": "Checkout", "ar": "إتمام الطلب"},
    "about": {"en": "About Us", "ar": "من نحن"},
    "service": {"en": "Customer Service", "ar": "خدمة العملاء"},
    "categories": {"en": "Categories", "ar": "الأقسام"},
    "legal": {"en": "Legal", "ar": "قانوني"},
    "shop_by_category": {"en": "Shop by Category", "ar": "تسوق حسب القسم"},
    "flash_sale": {"en": "Flash sale", "ar": "عروض خاطفة"},
    "deals": {"en": "Deals of the Day", "ar": "عروض اليوم"},
    "best_seller": {"en": "Best Seller", "ar": "الأكثر مبيعاً"},
    "view_all": {"en": "View all", "ar": "عرض الكل"},
    "add_to_cart": {"en": "Add to cart", "ar": "أضف للسلة"},
    "shop_now": {"en": "Shop now", "ar": "تسوق الآن"},
    "hero_title": {"en": "Up to 50% off on selected items", "ar": "خصم حتى 50% على منتجات مختارة"},
    "hero_text": {"en": "Electronics, fashion and home — delivered in Qatar.", "ar": "إلكترونيات وأزياء ومنزل — التوصيل في قطر."},
    "hours": {"en": "Hours", "ar": "ساعات"},
    "mins": {"en": "Mins", "ar": "دقائق"},
    "secs": {"en": "Secs", "ar": "ثوان"},
}

AREAS = {
    "en": ["Doha — West Bay", "Doha — The Pearl", "Doha — Lusail", "Doha — Al Sadd", "Al Wakrah", "Al Khor", "Al Rayyan"],
    "ar": ["الدوحة — الخليج الغربي", "الدوحة — اللؤلؤة", "الدوحة — لوسيل", "الدوحة — السد", "الوكر", "الخور", "الريان"],
}


def translate(key, lang="en"):
    row = STRINGS.get(key) or {}
    return row.get(lang) or row.get("en") or key


def install_i18n(app):
    @app.context_processor
    def inject_i18n():
        lang = session.get("lang", "en")
        return {
            "t": lambda key: translate(key, lang),
            "is_rtl": lang == "ar",
            "qatar_areas": AREAS["ar"] if lang == "ar" else AREAS["en"],
        }
