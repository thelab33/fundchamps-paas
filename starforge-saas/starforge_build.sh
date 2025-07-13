#!/bin/bash
echo "🚧 Starforge Build Pipeline: Assets + Tailwind + Config Check"

# Ensure the reports directory exists
mkdir -p reports

echo "🔁 Rebuilding Tailwind CSS..."
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/globals.css --minify && echo '✅ Tailwind rebuilt: globals.css'

echo "🔍 Checking Tailwind content coverage..."
grep -q '.text-white' app/static/css/globals.css && echo '✅ Tailwind styles confirmed in CSS' || echo '⚠️ No Tailwind styles detected!'

echo "📦 Verifying critical assets..."
ls -lh app/static/css/globals.css app/static/js/main.js > reports/assets_check.txt && cat reports/assets_check.txt

echo "⚙️ Dumping current config vars..."
FLASK_APP=manage.py flask shell <<< 'from flask import current_app; print("\n".join(f"{k}={v}" for k, v in current_app.config.items()))' > reports/config_vars.txt
