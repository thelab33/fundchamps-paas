from __future__ import annotations
import os
import pkgutil
import importlib
from pathlib import Path
from flask import Flask, request, g
from flask_cors import CORS

# Core extensions
from .extensions import db, migrate, socketio

def create_app(config_class: str | object | None = None) -> Flask:
    """
    Flask application factory for Connect ATX Elite PaaS.
    """
    app = Flask(
        __name__,
        static_folder="static",
        static_url_path="/static",
        template_folder="templates"
    )

    # Jinja fallback for _() calls
    try:
        from flask_babel import gettext as _
    except ImportError:
        _ = lambda s, **kwargs: s
    app.jinja_env.globals['_'] = _

    # ─── Load Configuration ────────────────────────────────────────
    cfg_path = (
        config_class
        if isinstance(config_class, str) or config_class is not None
        else os.getenv("FLASK_CONFIG", "config.ProductionConfig")
    )
    app.config.from_object(cfg_path)

    # Initialize config hooks (logging, Sentry, etc.)
    try:
        import config as cfg_module
        if hasattr(cfg_module, "init_app"):
            cfg_module.init_app(app)
    except Exception as e:
        app.logger.debug("No config.init_app available or failed; skipping", exc_info=True)

    # ─── CORS ───────────────────────────────────────────────────────
    cors_origins = app.config.get("CORS_ORIGINS", "*")
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": cors_origins}})

    # ─── Initialize Extensions ─────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins=cors_origins)

    # ─── Auto-discover and import models ───────────────────────────
    with app.app_context():
        models_dir = Path(__file__).parent / "models"
        if models_dir.exists():
            for module in pkgutil.iter_modules([str(models_dir)]):
                importlib.import_module(f"{app.import_name}.models.{module.name}")

    # ─── Register Blueprints ───────────────────────────────────────
    from app.routes.main import main_bp
    from app.routes.api import api_bp
    from app.routes.sms import sms_bp
    from app.routes.stripe_routes import stripe_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(sms_bp, url_prefix="/sms")
    app.register_blueprint(stripe_bp)

    try:
        from app.admin.routes import admin as admin_bp
        app.register_blueprint(admin_bp, url_prefix="/admin")
    except ImportError:
        app.logger.warning("Admin blueprint not found; skipping admin routes.")

    # ─── Health Check Endpoint ─────────────────────────────────────
    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "message": f"{app.name} live!"}

    # ─── Context Processor ─────────────────────────────────────────
    @app.context_processor
    def inject_globals():
        team = None
        try:
            from app.models.team import Team
            team = Team.query.filter_by(
                slug=app.config.get("DEFAULT_TEAM_SLUG", "connect-atx-elite")
            ).first()
        except Exception:
            app.logger.debug("Team not available; context 'team' set to None.", exc_info=True)

        try:
            from flask_login import current_user
        except ImportError:
            current_user = None

        return {
            "config": app.config,
            "team": team,
            "current_user": current_user,
            "analytics_id": app.config.get("GA_MEASUREMENT_ID"),
            "request": request,
            "g": g,
            "_": _,
        }

    return app

