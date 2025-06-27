#!/bin/bash
# 🚀 Starforge All-in-One Deploy Script — by Angel Rodriguez Jr.

set -e

echo "🌟 Starforge: Starting deploy mode..."

# 1. Set env
export FLASK_APP=run.py
export FLASK_ENV=production
export SENTRY_DSN="${SENTRY_DSN:-}"
export PORT=${PORT:-5000}
export ADMIN_URL=${ADMIN_URL:-/admin}

# 2. Collect static assets (Tailwind + JS)
echo "✨ Building static assets..."
npm run build || { echo "❌ npm build failed"; exit 1; }

# 3. Migrate DB
echo "🛠️ Upgrading database (Flask-Migrate)..."
flask db upgrade

# 4. Seed demo data if needed
if [ "$1" = "--demo" ]; then
    echo "🧬 Seeding demo data..."
    flask demo-data
fi

# 5. Healthcheck (simple ping)
echo "🩺 Healthcheck:"
curl -sf "http://localhost:${PORT}${ADMIN_URL}/healthz" || echo "(Will pass after launch)"

# 6. Sentry test (raise a handled error)
if [[ -n "$SENTRY_DSN" ]]; then
    echo "🛡️ Testing Sentry..."
    flask shell -c 'raise Exception("Starforge Sentry Test Error")' || true
fi

# 7. Launch with Gunicorn + eventlet (for Flask-SocketIO)
echo "🚦 Launching Gunicorn (eventlet, prod ready!)..."
exec gunicorn --worker-class eventlet -w 1 -b 0.0.0.0:${PORT} run:app

# 8. Done
echo "🎉 Deploy complete! Visit:"
echo "   • Admin: http://localhost:${PORT}${ADMIN_URL}"
echo "   • Health: http://localhost:${PORT}${ADMIN_URL}/healthz"

