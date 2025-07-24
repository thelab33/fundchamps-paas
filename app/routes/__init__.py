from typing import TYPE_CHECKING
from flask import Blueprint, Flask
from app.cli import starforge

# Import blueprints; fallback to None if not present to avoid import errors during partial dev
try:
    from .main import main_bp
except ImportError:
    main_bp = None

try:
    from .api import api_bp
except ImportError:
    api_bp = None

try:
    from .sms import sms_bp
except ImportError:
    sms_bp = None

try:
    from .stripe_routes import stripe_bp
except ImportError:
    stripe_bp = None

try:
    from .webhooks import webhook_bp
except ImportError:
    webhook_bp = None


# Fallback homepage if main_bp does not define "/"
fallback = Blueprint("fallback", __name__)

@fallback.route("/")
def default_root():
    """Fallback route when the main route '/' is not defined in main_bp."""
    return "✅ FundChamps SaaS backend is running. Add a homepage to 'main_bp'."

def register_blueprints(app: Flask) -> None:
    """
    Register all blueprints and CLI commands to the Flask app.

    This includes main, API, SMS, Stripe, webhook blueprints, and CLI commands.

    Args:
        app (Flask): The Flask app instance.
    """
    print("🔌 Registering blueprints and CLI commands...")

    # Register CLI command group
    app.cli.add_command(starforge)
    print("🛠️ Registered CLI command group: starforge")

    # Register blueprints if available
    if main_bp:
        app.register_blueprint(main_bp)
        print("🧩 Registered blueprint: main_bp")
    else:
        print("⚠️ main_bp not found; skipping.")

    if api_bp:
        app.register_blueprint(api_bp, url_prefix="/api")
        print("🧩 Registered blueprint: api_bp")
    else:
        print("⚠️ api_bp not found; skipping.")

    if sms_bp:
        app.register_blueprint(sms_bp, url_prefix="/sms")
        print("🧩 Registered blueprint: sms_bp")
    else:
        print("⚠️ sms_bp not found; skipping.")

    if stripe_bp:
        app.register_blueprint(stripe_bp, url_prefix="/stripe")
        print("🧩 Registered blueprint: stripe_bp")
    else:
        print("⚠️ stripe_bp not found; skipping.")

    if webhook_bp:
        app.register_blueprint(webhook_bp, url_prefix="/webhook")
        print("🧩 Registered blueprint: webhook_bp")
    else:
        print("⚠️ webhook_bp not found; skipping.")

    # Always register fallback last (acts only if main '/' missing)
    app.register_blueprint(fallback)
    print("🧩 Registered fallback homepage blueprint")

    print("🔌 All blueprints and CLI commands registered successfully.")

