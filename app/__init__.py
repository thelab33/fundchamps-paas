"""
app/__init__.py – Starforge core bootstrap
-----------------------------------------
Usage patterns:

    from app import db
    from app import socketio
    from app import create_app
"""

from __future__ import annotations

import os, pkgutil, importlib
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_cors  import CORS

# ── Core extensions ──────────────────────────────────────────────
db       = SQLAlchemy()
migrate  = Migrate()
socketio = SocketIO(cors_allowed_origins="*")   # gevent/uvicorn autodetected

__all__ = ["db", "migrate", "socketio", "create_app"]


# ── Factory ──────────────────────────────────────────────────────
def create_app(config_class: str | object | None = None) -> Flask:
    """Flask application factory with dynamic model discovery."""
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Smart config loader (str path, object, env var, or fallback)
    if isinstance(config_class, str):
        app.config.from_object(config_class)
    elif config_class is not None:
        app.config.from_object(config_class)
    else:
        app.config.from_object(os.getenv("FLASK_CONFIG") or "config.DevelopmentConfig")

    # CORS (public API)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

    # Initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)

    # ── Auto-import every model file so SQLAlchemy sees each table ──
    with app.app_context():
        models_path = Path(__file__).parent / "models"
        for mod in pkgutil.iter_modules([str(models_path)]):
            importlib.import_module(f"app.models.{mod.name}")

    # ── Blueprints ────────────────────────────────────────────────
    from app.routes import main_bp, api_bp, sms_bp
    from app.routes.stripe_routes import stripe_bp         #  ← NEW
    try:
        from app.admin.routes import admin as admin_bp
    except ImportError:
        admin_bp = None

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp,      url_prefix="/api")
    app.register_blueprint(sms_bp,      url_prefix="/sms")
    app.register_blueprint(stripe_bp)                     #  ← NEW
    if admin_bp:
        app.register_blueprint(admin_bp, url_prefix="/admin")

    # Simple health-check
    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "message": "Starforge Flask live!"}

    return app

