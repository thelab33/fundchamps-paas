import logging  # Ensure logging is imported
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
    This function initializes the app with configuration, extensions, routes, and error handling.
    
    Args:
        config_class (str): The import path for the config class. Defaults to DevelopmentConfig.

    Returns:
        Flask app instance
    """
    
    # ──────────────── Define Static Folder Path ────────────────
    static_folder_path = '/home/cyberboyz/connectatx-fundraiser/app/static'
    static_url_path = '/static'

    # Create Flask app instance
    app = Flask(
        __name__,
        static_folder=static_folder_path,
        static_url_path=static_url_path
    )

    # Load configuration from the provided config class
    app.config.from_object(config_class)

    # ──────────────── Initialize Extensions ────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)
    
    # ──────────────── Enable Cross-Origin Resource Sharing ────────────────
    # Allow CORS for API routes to support cross-origin requests
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # ──────────────── Global Template Context ────────────────
    # Inject global variables (like current_user and current time) into templates
    from flask_login import current_user
    from flask_babel import _

    @app.context_processor
    def inject_globals() -> dict[str, Any]:
        """
        Inject global variables (current_user, translation function, current time) into templates.
        """
        return dict(current_user=current_user, _=_, now=datetime.utcnow())

    # ──────────────── Register Blueprints ────────────────
    # Register the main blueprint for UI routes and the API blueprint
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    # ──────────────── API Error Handlers ────────────────
    # Register custom error handlers for API routes
    try:
        from app.routes.api import register_error_handlers
        register_error_handlers(app)
    except ImportError:
        logging.warning("No custom error handlers found for the API routes.")

    # ──────────────── CLI Commands (Optional) ────────────────
    # Register CLI commands if available
    try:
        from app.commands import register_commands
        register_commands(app)
    except ImportError:
        logging.warning("No CLI commands found for the app.")

    # ──────────────── Startup Banner ────────────────
    # Print a startup banner with app details for debugging and CI/CD purposes
    print("=" * 60)
    print(f"🚀 Starforge App Booted | ENV={app.config.get('ENV')} | DEBUG={app.debug}")
    print(f"📦 DB URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print("=" * 60)

    return app

