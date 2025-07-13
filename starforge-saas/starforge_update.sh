#!/usr/bin/env bash
set -euo pipefail
echo "🌟 Starforge Blueprint & Static Asset Updater"

# Set working dir
cd "$(dirname "$0")"

echo "🔁 Ensuring correct blueprint imports in app/routes/__init__.py..."
cat > app/routes/__init__.py <<EOF
from .main import main_bp
from .api import api_bp
from .sms import sms_bp
from .stripe_routes import stripe_bp
from .webhooks import webhooks_bp
EOF

echo "✅ app/routes/__init__.py updated."

echo "🔁 Updating Tailwind static CSS reference in base.html..."
BASE_HTML="app/templates/base.html"
sed -i.bak -E 's|href=\{\{ url_for\(.*tailwind.*\) \}\}|href=\{\{ url_for('static', filename='css/globals.css') \}\}|' "$BASE_HTML"
echo "✅ Tailwind CSS path updated in base.html."

echo "🔁 Validating blueprint registrations in app/__init__.py..."
# Append missing registrations (idempotent block)
INIT_FILE="app/__init__.py"
BLOCK=$(cat <<'BLOCK'
    from app.routes import main_bp, api_bp, sms_bp, stripe_bp, webhooks_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(sms_bp, url_prefix="/sms")
    app.register_blueprint(stripe_bp)
    app.register_blueprint(webhooks_bp)
BLOCK
)

grep -q "main_bp" "$INIT_FILE" || echo "$BLOCK" >> "$INIT_FILE"
echo "✅ Blueprint registration ensured."

echo "🔁 Injecting model auto-imports in app/models/__init__.py..."
cat > app/models/__init__.py <<EOF
from .campaign_goal import CampaignGoal
from .example import Example
from .player import Player
from .sponsor import Sponsor
from .team import Team
from .transaction import Transaction
from .user import User
EOF
echo "✅ app/models/__init__.py cleaned and rebuilt."

echo "🧼 Removing old Tailwind references..."
grep -l "tailwind.min.css" app/templates/*.html | xargs -r sed -i '/tailwind.min.css/d'
echo "✅ Legacy tailwind.min.css references removed."

echo "🚀 Done. Starforge structure and static assets are now elite-grade."
