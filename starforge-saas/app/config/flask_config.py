import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()


class Config:
    """
    Base configuration class containing default settings for the app.
    """

    # Secret Key (for session management, CSRF protection)
    SECRET_KEY = os.environ.get("SECRET_KEY") or "mysecretkey"

    # Database Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration (for Flask-Mail)
    MAIL_SERVER = os.environ.get(
        "MAIL_SERVER", "smtp.gmail.com"
    )  # Default to Gmail if not set
    MAIL_PORT = os.environ.get("MAIL_PORT", 587)  # Default to 587 (TLS)
    MAIL_USE_TLS = bool(
        os.environ.get("MAIL_USE_TLS", True)
    )  # Default to True if not set
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")

    # Security-related configuration
    SESSION_COOKIE_SECURE = True  # Cookie will only be sent over HTTPS
    REMEMBER_COOKIE_SECURE = True  # Ensure remember me cookies are only sent over HTTPS
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT") or "default_salt"

    @staticmethod
    def init_app(app):
        """
        Initialize any app-wide configuration here (e.g., logging, file storage).
        """
        pass


class DevelopmentConfig(Config):
    """
    Development environment configuration.
    """

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///dev.db"
    )

    # Additional configuration for development
    DEVELOPMENT = True
    ENV = "development"


class TestingConfig(Config):
    """
    Testing environment configuration.
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") or "sqlite:///test.db"
    )

    # Disabling the use of CSRF during testing
    CSRF_ENABLED = False
    ENV = "testing"


class ProductionConfig(Config):
    """
    Production environment configuration.
    """

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or "postgresql://localhost/production_db"
    )
    DEBUG = False
    ENV = "production"

    # Production-specific configurations
    LOGGING_LEVEL = "INFO"  # Control the logging level
    LOGGING_FILE = "production.log"  # Log file path for production logs


class StagingConfig(ProductionConfig):
    """
    Staging environment configuration.
    """

    ENV = "staging"
    DEBUG = True  # Enable debug in staging
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI") or "postgresql://localhost/staging_db"
    )


# Dictionary to hold the environment-specific configurations
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "staging": StagingConfig,
}
