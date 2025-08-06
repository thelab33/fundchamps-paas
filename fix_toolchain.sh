#!/usr/bin/env bash
set -euo pipefail

echo "➕ Backing up package.json"
cp package.json package.json.bak.$(date +%F-%H%M%S)

# Patch devDependencies versions (ensures valid versions)
node - <<'NODE'
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
pkg.devDependencies = Object.assign({}, pkg.devDependencies, {
  "cross-env": "^10.0.0",
  "npm-run-all": "^4.1.5",
  "postcss": "^8.5.6",
  "postcss-cli": "^11.0.1",
  "tailwindcss": "^3.4.17",
  "autoprefixer": "^10.4.21",
  "esbuild": "^0.25.8",
  "husky": "^8.0.0",
  "stylelint": "^16.8.0",
  "stylelint-config-standard": "^36.0.0",
  "stylelint-config-prettier": "^9.0.5",
  "stylelint-config-tailwindcss": "^1.0.0",
  "stylelint-order": "^6.0.4",
  "stylelint-tailwindcss": "^0.5.0"
});
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
console.log("✓ package.json devDependencies patched");
NODE

# Ensure stylelint ignore exists
cat > .stylelintignore <<'EOF'
**/*.min.css
**/*.map
dist/**
build/**
app/static/css/tailwind.min.css
app/static/css/**/*.min.css
app/static/css/vendor/**
EOF
echo "✓ .stylelintignore written"

echo "📦 Installing deps (skip failing lifecycle scripts)…"
npm i --ignore-scripts

echo "🔧 Setting up husky…"
npx husky install || true

echo "🏗️ Building assets…"
npm run build:fast || { echo "Build failed, trying direct compile"; \
  npx postcss app/static/css/input.css -o app/static/css/tailwind.min.css; \
  npx esbuild app/static/js/main.js --bundle --format=esm --minify --sourcemap --outfile=app/static/js/main.js --allow-overwrite; }

echo "✅ Done. Try: npm run dev:app"

