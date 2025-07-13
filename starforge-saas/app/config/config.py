# config.py — Environment-driven configuration for Connect ATX Elite
from __future__ import annotations
import os
import json
import logging
from datetime import timedelta
from pathlib import Path
from typing import Final, Type, Iterable

# ────────────── Helpers ───────────────────────────────────────────
# BASE_DIR is your project root
BASE_DIR: Final[Path] = Path(__file__).resolve().parent

def _bool(key: str, default: bool = False) -> bool:
    return os.getenv(key, str(int(default))).strip().lower() in {"1", "true", "yes", "on"}

def _int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, default))
    except ValueError:
        raise RuntimeError(f"Env var {key} must be integer, got: {os.getenv(key)}")

def _default_db_uri() -> str:
    # point at app/data/app.db
    return os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'app' / 'data' / 'app.db'}"
    )

# ────────────── Base Configuration ─────────────────────────────────
class BaseConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-before-prod")
    ENV: Final[str] = os.getenv("FLASK_ENV", "production")
    DEBUG: bool = _bool("DEBUG", False)
    LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO").upper()
    PERMANENT_SESSION_LIFETIME: timedelta = timedelta(days=7)

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = _default_db_uri()

    # Payments
    STRIPE_SECRET_KEY: str | None = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY: str | None = os.getenv("STRIPE_PUBLIC_KEY")

    # Email
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT: int = _int("MAIL_PORT", 587)
    MAIL_USE_TLS: bool = _bool("MAIL_USE_TLS", True)
    MAIL_USERNAME: str | None = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = os.getenv("MAIL_DEFAULT_SENDER", "noreply@connectatxelite.com")

    # Feature toggles
    FEATURE_DARK_MODE: bool = _bool("FEATURE_DARK_MODE", True)

    # Branding
    BRAND_NAME: str = os.getenv("BRAND_NAME", "Connect ATX Elite")
    BRAND_TAGLINE: str = os.getenv(
        "BRAND_TAGLINE",
        "Family-run AAU basketball building future leaders in East Austin."
    )
    PRIMARY_COLOR: str = os.getenv("PRIMARY_COLOR", "#facc15")

    @classmethod
    def init_app(cls, app):
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
        )
        if _bool("PRINT_CONFIG", False):
            app.logger.info("Loaded configuration: %s", cls.__name__)
            print(json.dumps(
                {k: v for k, v in cls.__dict__.items() if k.isupper()},
                indent=2,
            ))

class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True

class TestingConfig(BaseConfig):
    ENV = "testing"
    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"

class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False
    SESSION_COOKIE_SECURE: bool = True

    REQUIRED_VARS: Final[Iterable[str]] = (
        "SECRET_KEY",
        "STRIPE_SECRET_KEY",
        "STRIPE_PUBLIC_KEY",
        "MAIL_SERVER",
        "MAIL_USERNAME",
        "MAIL_PASSWORD",
    )

    @classmethod
    def init_app(cls, app):
        super().init_app(app)
        missing = [var for var in cls.REQUIRED_VARS if not os.getenv(var)]
        if missing:
            raise RuntimeError(f"Missing required environment vars: {', '.join(missing)}")

# Selector
config_map: dict[str, Type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def get_config() -> Type[BaseConfig]:
    return config_map.get(os.getenv("FLASK_ENV", "production"), ProductionConfig)

config = get_config()

