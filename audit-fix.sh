#!/bin/bash
set -e

echo "🔍 Starting Production Grade Frontend Audit & Fix..."

# 1. Prettier Formatting
echo "💅 Running Prettier formatting..."
npx prettier --write "app/static/js/**/*.js" "app/static/css/**/*.css" "app/templates/**/*.html"

# 2. ESLint Lint + Fix
echo "🔧 Running ESLint for JS..."
npx eslint "app/static/js/**/*.js" --fix || true

# 3. Stylelint CSS Lint + Fix
echo "🎨 Running Stylelint for CSS..."
npx stylelint "app/static/css/**/*.css" --fix || true

# 4. HTMLHint Lint (reports only)
echo "📄 Running HTMLHint for HTML linting..."
npx htmlhint "app/templates/**/*.html" --config .htmlhintrc

# 5. Tailwind CSS build for production
echo "🌬 Building Tailwind CSS for production..."
NODE_ENV=production npx tailwindcss -c tailwind.config.cjs -i app/static/globals.css -o app/static/tailwind.min.css --minify

echo "✅ Audit & fixes complete!"
