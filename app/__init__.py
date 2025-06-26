import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")

def create_app(config_class=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class or os.getenv("FLASK_CONFIG") or "config.DevelopmentConfig")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.sms import sms_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(sms_bp, url_prefix="/sms")

    return app
