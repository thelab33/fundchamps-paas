from flask import Flask
from datetime import datetime
from app.extensions import db, migrate, socketio, login_manager, babel
from app.routes.main import main_bp
from app.routes.api import api_bp
from flask_cors import CORS
from typing import Any

def create_app(config_class: str = "app.config.DevelopmentConfig") -> Flask:
    """
    Flask application factory.
    Args:
        config_class (str): Import path for config class (default: Development).
    Returns:
        Flask app instance.
    """

    app = Flask(__name__)
    app.config.from_object(config_class)

    # ──────────────── Initialize Extensions ────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ──────────────── Global Template Context ────────────────
    from flask_login import current_user
    from flask_babel import _

    @app.context_processor
    def inject_globals() -> dict[str, Any]:
        return dict(current_user=current_user, _=_, now=datetime.utcnow())

    # ──────────────── Register Blueprints ────────────────
    app.register_blueprint(main_bp)    # UI routes (no prefix)
    app.register_blueprint(api_bp)     # API routes (prefixed in api_bp)

    # ──────────────── API Error Handlers ────────────────
    try:
        from app.routes.api import register_error_handlers
        register_error_handlers(app)
    except ImportError:
        pass  # No custom error handlers found

    # ──────────────── CLI Commands (Optional) ────────────────
    try:
        from app.commands import register_commands
        register_commands(app)
    except ImportError:
        pass  # No CLI commands registered

    # ──────────────── Startup Banner ────────────────
    print("=" * 60)
    print(f"🚀 Starforge App Booted | ENV={app.config.get('ENV')} | DEBUG={app.debug}")
    print(f"📦 DB URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print("=" * 60)

    return app

