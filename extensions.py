from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


class _LoginManager(LoginManager):
    def init_app(self, app, add_context_processor=True):
        super().init_app(app, add_context_processor=add_context_processor)
        for mod, fn in (
            ("admin_panel", "register_admin"),
            ("i18n", "install_i18n"),
            ("newsletter", "install_newsletter"),
            ("catalog", "install_catalog"),
            ("skipcash", "install_skipcash"),
            ("sadad", "install_sadad"),
        ):
            try:
                m = __import__(mod, fromlist=[fn])
                getattr(m, fn)(app)
            except Exception:
                pass


login_manager = _LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "info"
