from __future__ import annotations

"""
Starforge Flask application factory.

- Robust config loading with legacy fallback
- Optional extensions (Login, Babel, CLI) loaded if installed
- Unified error handling for API-ish requests
- Request ID middleware
- Jinja filters (comma, commafy)
- Blueprints: main (required), api/sms/admin (optional)
"""

from typing import Any, Optional, Type
import logging
import os
from datetime import datetime
from importlib import import_module
from pathlib import Path
from uuid import uuid4

from dotenv import load_dotenv
from flask import Flask, g, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

# Load .env early
load_dotenv()

# Project root (connectatx-fundraiser/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Core extensions (must exist)
from app.extensions import db, migrate, socketio, mail  # noqa: E402

# Optional extensions
USE_LOGIN = USE_BABEL = USE_CLI = False
try:
    from flask_login import LoginManager, current_user  # type: ignore
    login_manager: Optional[LoginManager] = LoginManager()
    USE_LOGIN = True
except Exception:  # pragma: no cover
    login_manager = None

try:
    from flask_babel import Babel, _ as _t  # type: ignore
    USE_BABEL = True
except Exception:  # pragma: no cover
    Babel = None  # type: ignore[assignment]
    _t = lambda s: s  # noqa: E731

try:
    from app.cli import starforge  # type: ignore
    USE_CLI = True
except Exception:  # pragma: no cover
    starforge = None  # type: ignore[assignment]


# ─────────────────────────── helpers ─────────────────────────── #

def _resolve_config(target: str | Type[Any]) -> str | Type[Any]:
    """
    Accepts a dotted path or a config class; returns something
    Flask's `from_object` understands. Supports legacy path.
    """
    if isinstance(target, str):
        if target == "app.config.config.DevelopmentConfig":
            return "app.config.DevelopmentConfig"
        return target
    return target


def _json_error(message: str, status: int, **extra: Any):
    payload = {"status": "error", "message": message, **extra}
    return jsonify(payload), status


def _file_mtime_version(path: Path) -> int:
    try:
        return int(path.stat().st_mtime)
    except Exception:
        return int(datetime.utcnow().timestamp())


def _configure_logging(app: Flask) -> None:
    # Avoid duplicate handlers when reloader restarts
    root = logging.getLogger()
    if not root.handlers:
        logging.basicConfig(
            level=app.config.get("LOG_LEVEL", "INFO"),
            format="%(asctime)s %(levelname)s %(name)s %(message)s",
        )
    logging.getLogger("werkzeug").setLevel(app.config.get("WERKZEUG_LOG_LEVEL", "WARNING"))
    logging.info("Loaded configuration: %s | DEBUG=%s", app.config.get("ENV", "unknown"), app.debug)
    logging.info("DB: %s", app.config.get("SQLALCHEMY_DATABASE_URI", "<unset>"))


# ───────────────────── application factory ───────────────────── #

def create_app(config_class: str | Type[Any] | None = None) -> Flask:
    """Create and configure the Starforge Flask app."""
    app = Flask(
        __name__,
        static_folder=str(BASE_DIR / "app/static"),
        template_folder=str(BASE_DIR / "app/templates"),
    )

    # 1) Config
    default_cfg = os.getenv("FLASK_CONFIG", "app.config.DevelopmentConfig")
    target_cfg = _resolve_config(config_class or default_cfg)
    try:
        app.config.from_object(target_cfg)
    except (ImportError, AttributeError, ModuleNotFoundError) as exc:
        legacy = "app.config.config.DevelopmentConfig"
        if isinstance(target_cfg, str) and target_cfg != legacy:
            try:
                app.config.from_object(legacy)
            except Exception:
                raise RuntimeError(f"❌ Invalid FLASK_CONFIG '{target_cfg}': {exc}") from exc
        else:
            raise RuntimeError(f"❌ Invalid FLASK_CONFIG '{target_cfg}': {exc}") from exc

    # 2) Logging
    _configure_logging(app)

    # 3) CORS
    default_origin = "*" if app.config.get("ENV") != "production" else os.getenv(
        "PRIMARY_ORIGIN", "https://connect-atx-elite.com"
    )
    cors_origins = os.getenv("CORS_ORIGINS", default_origin)
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": cors_origins}})

    # 4) Security headers / CSP (optional)
    if app.config.get("ENV") == "production":
        try:
            from flask_talisman import Talisman  # type: ignore
            # Keep CSP None by default to avoid breaking inline/3rd-party;
            # tighten once you self-host assets.
            Talisman(app, content_security_policy=None)
        except Exception:
            logging.warning("⚠️ flask-talisman not installed – skipping CSP setup")

    # 5) Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins=cors_origins)
    mail.init_app(app)

    # 6) Request ID middleware
    @app.before_request
    def _assign_request_id() -> None:
        g.request_id = request.headers.get("X-Request-ID", uuid4().hex)

    @app.after_request
    def _inject_request_id(resp):
        resp.headers.setdefault("X-Request-ID", getattr(g, "request_id", uuid4().hex))
        # A few conservative security headers (non-breaking)
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        return resp

    # 7) Login (optional)
    if USE_LOGIN and login_manager:
        login_manager.init_app(app)
        try:
            from app.models.user import User  # local import to avoid circulars
        except Exception as exc:
            logging.warning("Login enabled but User model import failed: %s", exc)
            User = None  # type: ignore

        @login_manager.user_loader
        def load_user(user_id: str):
            if not User:
                return None
            try:
                return User.query.get(int(user_id))
            except Exception:
                return None

        @app.context_processor
        def _inject_user() -> dict[str, Any]:
            return {"current_user": current_user}
    else:
        @app.context_processor
        def _inject_user() -> dict[str, Any]:
            class _Anon:
                is_authenticated = False

                def __bool__(self) -> bool:
                    return False
            return {"current_user": _Anon()}

    # 8) Babel (optional)
    if USE_BABEL and Babel:
        babel = Babel(app)

        @app.context_processor
        def _inject_babel() -> dict[str, Any]:
            return {"_": _t}
    else:
        @app.context_processor
        def _inject_noop() -> dict[str, Any]:
            return {"_": (lambda s: s)}

    # 9) CLI (optional)
    if USE_CLI and starforge:
        app.cli.add_command(starforge)

    # 10) Template context: env, now, team, asset_version
    @app.context_processor
    def _inject_env() -> dict[str, Any]:
        return {"app_env": app.config.get("ENV"), "app_config": app.config}

    @app.context_processor
    def _inject_now() -> dict[str, Any]:
        return {"now": datetime.utcnow}

    @app.context_processor
    def _inject_team() -> dict[str, Any]:
        class _Empty:
            def __getattr__(self, _):  # type: ignore[no-untyped-def]
                return None

            def __str__(self) -> str:
                return ""
        return {"team": _Empty()}

    @app.context_processor
    def _inject_asset_versions() -> dict[str, Any]:
        css = Path(app.static_folder or "app/static") / "css" / "tailwind.min.css"
        js = Path(app.static_folder or "app/static") / "js" / "main.js"
        return {"asset_version": max(_file_mtime_version(css), _file_mtime_version(js))}

    # 11) Jinja filters
    def _comma_like(val: Any) -> Any:
        try:
            return f"{int(val):,}"
        except (ValueError, TypeError):
            try:
                return f"{float(val):,}"
            except (ValueError, TypeError):
                return val

    app.add_template_filter(_comma_like, "comma")

    # commafy (prefer your implementation, fall back to _comma_like)
    try:
        from .filters import commafy  # your custom filter
        app.jinja_env.filters["commafy"] = commafy
    except Exception:
        app.jinja_env.filters["commafy"] = _comma_like  # graceful fallback

    # 12) Error handling
    def _wants_json() -> bool:
        return (
            "application/json" in request.headers.get("Accept", "")
            or request.path.startswith("/api")
        )

    @app.errorhandler(HTTPException)
    def _handle_http_exc(err: HTTPException):
        if _wants_json():
            return _json_error(err.description or err.name, err.code or 500)
        return err

    @app.errorhandler(Exception)
    def _handle_uncaught(err: Exception):
        logging.exception("Unhandled error: %s", err)
        if _wants_json():
            return _json_error("Internal Server Error", 500, request_id=getattr(g, "request_id", None))
        return err

    # 13) Blueprints
    from app.routes import main_bp  # required
    app.register_blueprint(main_bp)

    for dotted, prefix in (("app.api", "/api"), ("app.sms", "/sms")):
        try:
            mod = import_module(dotted)
            bp = getattr(mod, "api_bp", None) or getattr(mod, "bp", None)
            if not bp:
                raise AttributeError("No blueprint named 'api_bp' or 'bp'")
            app.register_blueprint(bp, url_prefix=prefix)
        except (ModuleNotFoundError, AttributeError) as exc:
            logging.warning("⚠️ Blueprint %s not registered: %s", dotted, exc)

    try:
        admin_bp = import_module("app.admin.routes").admin  # type: ignore[attr-defined]
        app.register_blueprint(admin_bp, url_prefix="/admin")
    except (ModuleNotFoundError, AttributeError) as exc:
        logging.info("Admin dashboard not found – skipping (%s)", exc)

    # 14) Health & version
    @app.get("/healthz")
    def _healthz():
        return {
            "status": "ok",
            "message": "Starforge Flask live!",
            "request_id": getattr(g, "request_id", None),
        }

    @app.get("/version")
    def _version():
        return {
            "version": os.getenv("GIT_COMMIT", "dev"),
            "env": app.config.get("ENV"),
        }

    # 15) Launch banner
    print(
        "\n".join(
            (
                "┌────────────────────────────────────────────┐",
                "│  🌟 Starforge SaaS: Flask Ready to Launch  │",
                f"│  ENV = {app.config.get('ENV', 'unknown'):<12}   DEBUG = {str(app.debug):<5}   │",
                "└────────────────────────────────────────────┘",
            )
        )
    )

    return app


__all__ = ["create_app"]

