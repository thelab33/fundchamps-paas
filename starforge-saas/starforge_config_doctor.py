#!/usr/bin/env python3
import os
import re
from urllib.parse import urlparse

REQUIRED_CONFIG = {
    "SECRET_KEY": {"desc": "Flask session secret", "suggest": "super-secret-key"},
    "SQLALCHEMY_DATABASE_URI": {
        "desc": "SQLAlchemy DB URI",
        "suggest": "mysql+pymysql://user:password@host/db",
    },
    "STRIPE_SECRET_KEY": {
        "desc": "Stripe Secret Key",
        "pattern": r"^sk_(test|live)_",
        "suggest": "sk_live_xxx",
    },
    "STRIPE_PUBLIC_KEY": {
        "desc": "Stripe Public Key",
        "pattern": r"^pk_(test|live)_",
        "suggest": "pk_live_xxx",
    },
    "STRIPE_WEBHOOK_SECRET": {
        "desc": "Stripe Webhook Secret",
        "pattern": r"^whsec_",
        "suggest": "whsec_xxx",
    },
    "MAIL_SERVER": {"desc": "SMTP Server", "suggest": "smtp.sendgrid.net"},
    "MAIL_PORT": {"desc": "SMTP Port", "suggest": "587"},
    "MAIL_USE_TLS": {"desc": "SMTP TLS (1 or 0)", "suggest": "1"},
    "MAIL_USERNAME": {"desc": "SMTP Username", "suggest": "apikey"},
    "MAIL_PASSWORD": {"desc": "SMTP Password/API Key", "suggest": "sendgrid_api_key"},
    "MAIL_DEFAULT_SENDER": {
        "desc": "Default sender",
        "suggest": '"Team <team@email.com>"',
    },
    "FLASK_ENV": {"desc": "Flask environment", "suggest": "production"},
    "LOG_LEVEL": {"desc": "Logging level", "suggest": "INFO"},
    # ... Add more as needed
}

OPTIONAL_CONFIG = {
    "REDIS_URL": {
        "desc": "Redis cache URL",
        "suggest": "redis://user:pass@host:6379/0",
    },
    "SENTRY_DSN": {"desc": "Sentry DSN", "suggest": "https://public@sentry.io/123"},
    "SLACK_WEBHOOK_URL": {
        "desc": "Slack Webhook",
        "suggest": "https://hooks.slack.com/services/XXX/YYY/ZZZ",
    },
    "OPENAI_API_KEY": {"desc": "OpenAI API Key", "suggest": "sk-xxxx"},
    "DOMAIN": {
        "desc": "Site domain for Stripe URLs",
        "suggest": "https://yourdomain.com",
    },
    "FEATURE_CONFETTI": {"desc": "Feature flag: Confetti", "suggest": "1"},
    "FEATURE_DARK_MODE": {"desc": "Feature flag: Dark mode", "suggest": "1"},
    "FEATURE_AI_THANK_YOU": {"desc": "Feature flag: AI Thank You", "suggest": "0"},
}


def check_url(val):
    try:
        result = urlparse(val)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def check_config():
    print("🔍 Starforge Config Doctor")
    print("=" * 40)

    errors = 0

    for key, meta in REQUIRED_CONFIG.items():
        val = os.getenv(key)
        if not val:
            print(f"❌ MISSING: {key:25} — {meta['desc']}")
            print(f"   Example: {meta['suggest']}")
            errors += 1
        else:
            # Pattern check
            if "pattern" in meta and not re.match(meta["pattern"], val):
                print(
                    f"⚠️  FORMAT:  {key:25} — Value \"{val}\" does not match pattern {meta['pattern']}"
                )
                errors += 1
            # URL check
            if "URL" in key and not check_url(val):
                print(f'⚠️  FORMAT:  {key:25} — Value "{val}" is not a valid URL')
                errors += 1

    print("\n(Checking optional config...)\n")
    for key, meta in OPTIONAL_CONFIG.items():
        val = os.getenv(key)
        if val:
            if "URL" in key and not check_url(val):
                print(
                    f'⚠️  OPTIONAL FORMAT: {key:25} — Value "{val}" is not a valid URL'
                )
        else:
            print(f"ℹ️  Optional: {key:25} — Not set ({meta['desc']})")

    print("=" * 40)
    if errors == 0:
        print("✅ All critical configs look good!")
    else:
        print(f"❗️Found {errors} issues. Please fix above.")

    print("\nTip: Set env variables via `.env` or your deployment config.")


if __name__ == "__main__":
    check_config()
