# app/cli/starforge.py


import click
from flask import current_app
from flask.cli import with_appcontext


@click.command("starforge-audit")
@with_appcontext
def audit_command():
    """🔍 Starforge SaaS Config & Blueprint Auditor."""
    print("\n🧪 [Starforge] Starting Flask SaaS Audit...\n")

    # Check core config keys
    required_keys = [
        "SECRET_KEY", "SQLALCHEMY_DATABASE_URI", "STRIPE_SECRET_KEY",
        "MAIL_SERVER", "MAIL_PORT", "MAIL_DEFAULT_SENDER"
    ]
    missing = [k for k in required_keys if not current_app.config.get(k)]

    print("✅ ENV:", current_app.config.get("ENV"))
    print("✅ DEBUG:", current_app.debug)
    print("✅ DB URI:", current_app.config.get("SQLALCHEMY_DATABASE_URI"))
    print("✅ Stripe:", "✅" if current_app.config.get("STRIPE_SECRET_KEY") else "❌ Missing")

    if missing:
        print("\n[⚠️] Missing critical config keys:")
        for key in missing:
            print(f"  ❌ {key}")
    else:
        print("\n✅ All critical configs loaded.")

    # Check blueprints
    print("\n🔍 Registered Blueprints:")
    for name in sorted(current_app.blueprints):
        print(f"  • {name}")

    # Check routes
    print("\n📌 Registered Routes:")
    for rule in sorted(current_app.url_map.iter_rules(), key=lambda r: r.rule):
        print(f"  {rule.rule:30} → {rule.endpoint}")

    print("\n✅ [Starforge] Audit Complete.\n")
