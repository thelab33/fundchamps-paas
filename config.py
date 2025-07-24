import os
import json
from datetime import timedelta
from typing import Final, Type, Dict, Any, Optional

# ──────────────────────── Directory Constants ────────────────────────
BASE_DIR: Final[str] = os.path.abspath(os.path.dirname(__file__))

# ──────────────────────── Env Helpers ────────────────────────
def _bool(key: str, default: bool = False) -> bool:
    """Safely get a boolean from environment."""
    val = os.getenv(key, str(int(default))).strip().lower()
    return val in {"1", "true", "yes", "on"}

def _int(key: str, default: int) -> int:
    """Safely get an integer from environment."""
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        raise RuntimeError(f"Env var {key} must be an integer, got: {os.getenv(key)}")

def _dict_from_env(keys: Dict[str, str]) -> Dict[str, str]:
    """Build a dict from env, using provided mapping of keys:env_vars."""
    return {k: os.getenv(env_var, v) for k, (env_var, v) in keys.items()}

# ──────────────────────── Base Config ────────────────────────
class BaseConfig:
    """Universal config: safe, overridable, SaaS-ready."""

    # Core Flask & App Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-before-prod")
    ENV: Final[str] = os.getenv("FLASK_ENV", "production")
    DEBUG: bool = _bool("DEBUG", False)
    TESTING: bool = _bool("TESTING", False)
    LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO").upper()
    PERMANENT_SESSION_LIFETIME: timedelta = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL") or f"sqlite:///{BASE_DIR}/app/data/app.db"

    # Stripe Integration
    STRIPE_SECRET_KEY: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY: Optional[str] = os.getenv("STRIPE_PUBLIC_KEY")

    # Mail/SMTP Settings
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT: int = _int("MAIL_PORT", 587)
    MAIL_USE_TLS: bool = _bool("MAIL_USE_TLS", True)
    MAIL_USERNAME: Optional[str] = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: Optional[str] = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = os.getenv("MAIL_DEFAULT_SENDER", "noreply@fundchamps.com")

    # Feature Flags & Branding
    FEATURE_DARK_MODE: bool = _bool("FEATURE_DARK_MODE", True)
    BRAND_NAME: str = os.getenv("BRAND_NAME", "FundChamps")
    BRAND_TAGLINE: str = os.getenv("BRAND_TAGLINE", "Empowering Youth Sports and Building Champions.")
    PRIMARY_COLOR: str = os.getenv("PRIMARY_COLOR", "#facc15")

    # Demo Team Defaults (used for onboarding, demo, or fallback)
    DEMO_TEAM_NAME: str = os.getenv("DEMO_TEAM_NAME", "Connect ATX Elite")
    DEMO_TEAM_TAGLINE: str = os.getenv("DEMO_TEAM_TAGLINE", "Family-run AAU basketball building future leaders in East Austin.")
    DEMO_TEAM_SCHEDULE_FILE: str = os.getenv("DEMO_TEAM_SCHEDULE_FILE", "ConnectATXElite-Schedule.ics")
    DEMO_TEAM_SOCIALS: Dict[str, str] = {
        "instagram": os.getenv("DEMO_TEAM_INSTAGRAM", "https://instagram.com/connectatxelite"),
        "facebook": os.getenv("DEMO_TEAM_FACEBOOK", "https://facebook.com/connectatxelite"),
        "twitter": os.getenv("DEMO_TEAM_TWITTER", "https://twitter.com/connectatxelite"),
    }

    @classmethod
    def init_app(cls, app: Any) -> None:
        """Attach config to Flask app & set up logging."""
        import logging
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        )
        if _bool("PRINT_CONFIG", False):
            app.logger.info(f"Loaded config: {cls.__name__}")
            print(json.dumps(
                {k: v for k, v in cls.__dict__.items() if k.isupper()},
                indent=2,
            ))

# ──────────────────────── Environments ────────────────────────
class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True

class TestingConfig(BaseConfig):
    ENV = "testing"
    TESTING = True
    DEBUG = True

class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    # SaaS-critical: Define what MUST be present to run in prod
    REQUIRED_VARS: Final = (
        "SECRET_KEY",
        "STRIPE_SECRET_KEY",
        "STRIPE_PUBLIC_KEY",
        "MAIL_SERVER",
        "MAIL_USERNAME",
        "MAIL_PASSWORD",
    )

    @classmethod
    def init_app(cls, app: Any) -> None:
        super().init_app(app)
        missing = [v for v in cls.REQUIRED_VARS if not os.getenv(v)]
        if missing:
            raise RuntimeError(f"Missing required environment vars: {', '.join(missing)}")

# ──────────────────────── Config Selector ────────────────────────
config_map: Dict[str, Type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def get_config() -> Type[BaseConfig]:
    """Return config class based on FLASK_ENV or default to Production."""
    env = os.getenv("FLASK_ENV", "production").lower()
    return config_map.get(env, ProductionConfig)

config = get_config()

