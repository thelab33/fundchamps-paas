#!/bin/bash
set -e

echo "🌀 Checking Tailwind config..."
[ -f tailwind.config.js ] || { echo "❌ tailwind.config.js not found."; exit 1; }

echo "🛠️  Rebuilding Tailwind CSS..."
npx tailwindcss -i ./app/static/css/input.css -o ./app/static/css/globals.css --minify

echo "✅ Tailwind build complete → app/static/css/globals.css"
