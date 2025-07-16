from flask import Flask
from datetime import datetime
from app.extensions import db, migrate, socketio, login_manager, babel
from app.routes.main import main_bp
from app.routes.api import api_bp
from flask_cors import CORS

def create_app(config_class="app.config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    login_manager.init_app(app)
    babel.init_app(app)

    # CORS - restrict to /api routes and allow all origins (adjust as needed)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Inject globals for templates (login user, translations, current time)
    from flask_login import current_user
    from flask_babel import _

    @app.context_processor
    def inject_globals():
        return dict(current_user=current_user, _=_, now=datetime.utcnow())

    # Register blueprints
    app.register_blueprint(main_bp)   # UI routes (no prefix)
    app.register_blueprint(api_bp)    # API routes, already have url_prefix="/api"

    # Register error handlers from api module
    from app.routes.api import register_error_handlers
    register_error_handlers(app)

    # Register CLI commands if any
    try:
        from app.commands import register_commands
        register_commands(app)
    except ImportError:
        pass

    # Startup logging
    print("=" * 60)
    print(f"🚀 Starforge App Booted | ENV={app.config.get('ENV')} | DEBUG={app.debug}")
    print(f"📦 DB URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print("=" * 60)

    return app

