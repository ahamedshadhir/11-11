from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


class _LoginManager(LoginManager):
    def init_app(self, app, add_context_processor=True):
        super().init_app(app, add_context_processor=add_context_processor)
        try:
            from admin_panel import register_admin
            register_admin(app)
        except Exception:
            pass
        try:
            from i18n import install_i18n
            install_i18n(app)
        except Exception:
            pass


login_manager = _LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Please log in to continue."
login_manager.login_message_category = "info"
