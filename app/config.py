import os
from datetime import timedelta
from typing import Final

# ────────────── Directory Constants ──────────────
BASE_DIR: Final = os.path.abspath(os.path.dirname(__file__))

# ────────────── Env Helpers ──────────────
def _bool(key: str, default: bool = False) -> bool:
    """
    Helper function to convert an environment variable to a boolean.
    Returns True if the environment variable is '1', 'true', 'yes', or 'on', else returns default.
    """
    return os.getenv(key, str(int(default))).strip().lower() in {"1", "true", "yes", "on"}

def _int(key: str, default: int) -> int:
    """
    Helper function to convert an environment variable to an integer.
    Raises an error if the value cannot be converted.
    """
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        raise RuntimeError(f"Env var {key} must be integer, got: {os.getenv(key)}")

# ────────────── Base Config ──────────────
class BaseConfig:
    """
    Base configuration class containing common settings for the app.
    Other configurations inherit from this class.
    """
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-before-prod")
    ENV: Final = os.getenv("FLASK_ENV", "production")
    DEBUG: bool = _bool("DEBUG", False)
    LOG_LEVEL: Final = os.getenv("LOG_LEVEL", "INFO").upper()
    PERMANENT_SESSION_LIFETIME: timedelta = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.getenv("DATABASE_URL") or f"sqlite:///{BASE_DIR}/app/data/app.db"

    # Stripe API keys (Optional)
    STRIPE_SECRET_KEY: str | None = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY: str | None = os.getenv("STRIPE_PUBLIC_KEY")

    # Mail server configuration
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT: int = _int("MAIL_PORT", 587)
    MAIL_USE_TLS: bool = _bool("MAIL_USE_TLS", True)
    MAIL_USERNAME: str | None = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = os.getenv("MAIL_DEFAULT_SENDER", "noreply@fundchamps.com")  # Updated for FundChamps

    # Feature flags and settings
    FEATURE_DARK_MODE: bool = _bool("FEATURE_DARK_MODE", True)

    # Branding settings
    BRAND_NAME: str = os.getenv("BRAND_NAME", "FundChamps")  # Default to FundChamps branding
    BRAND_TAGLINE: str = os.getenv("BRAND_TAGLINE", "Empowering Youth Sports and Building Champions.")
    PRIMARY_COLOR: str = os.getenv("PRIMARY_COLOR", "#facc15")

    # Demo team settings for Connect ATX Elite
    DEMO_TEAM_NAME: str = os.getenv("DEMO_TEAM_NAME", "Connect ATX Elite")
    DEMO_TEAM_TAGLINE: str = os.getenv("DEMO_TEAM_TAGLINE", "Family-run AAU basketball building future leaders in East Austin.")

    # Define TEAM_CONFIG for the demo team or production team settings
    TEAM_CONFIG = {
        "team_name": os.getenv("DEMO_TEAM_NAME", "Connect ATX Elite"),
        "team_tagline": os.getenv("DEMO_TEAM_TAGLINE", "Family-run AAU basketball building future leaders in East Austin."),
        "fundraising_goal": 10000,  # Example goal, can be updated via environment variables
        # Other team-related configuration settings...
    }

    @classmethod
    def init_app(cls, app):
        """
        Attach the configuration to the Flask app and set up logging.
        Logs the loaded config when PRINT_CONFIG is set.
        """
        import logging
        logging.basicConfig(
            level=cls.LOG_LEVEL,
            format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        )
        if _bool("PRINT_CONFIG", False):
            app.logger.info(f"Loaded config: {cls.__name__}")
            print(
                json.dumps(
                    {k: v for k, v in cls.__dict__.items() if k.isupper()},
                    indent=2,
                )
            )

# ────────────── Environment-Specific Configurations ──────────────
class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True

class TestingConfig(BaseConfig):
    ENV = "testing"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL") or f"sqlite:///{BASE_DIR}/app/data/app.db"

class ProductionConfig(BaseConfig):
    ENV = "production"
    DEBUG = False
    SESSION_COOKIE_SECURE = True

    REQUIRED_VARS: Final[tuple[str, ...]] = (
        "SECRET_KEY",
        "STRIPE_SECRET_KEY",
        "STRIPE_PUBLIC_KEY",
        "MAIL_SERVER",
        "MAIL_USERNAME",
        "MAIL_PASSWORD",
    )

    @classmethod
    def init_app(cls, app):
        """
        In production, check for required environment variables.
        """
        super().init_app(app)
        missing = [v for v in cls.REQUIRED_VARS if not os.getenv(v)]
        if missing:
            raise RuntimeError(
                f"Missing required environment vars: {', '.join(missing)}"
            )

# ────────────── Configuration Mapping ──────────────
config_map: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}

def get_config() -> type[BaseConfig]:
    """Return the appropriate config class based on FLASK_ENV."""
    return config_map.get(os.getenv("FLASK_ENV", "production"), ProductionConfig)

# Assign the appropriate config to `config`
config = get_config()

