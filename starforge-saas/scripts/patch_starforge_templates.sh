#!/usr/bin/env bash
set -euo pipefail

# Starforge Template Sanitizer & Patcher
# Usage: ./patch_starforge_templates.sh [templates_dir]

TEMPLATES_DIR="${1:-app/templates}"
BACKUP_DIR=".backup/templates_$(date +%Y%m%d_%H%M%S)"

echo "→ Backing up templates: $TEMPLATES_DIR → $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"
cp -r "$TEMPLATES_DIR" "$BACKUP_DIR"

echo "→ Patching sponsor_block.html…"
sed -i -E \
  -e "s@\{\{\s*sponsor\.logoifsponsor\.logo\.isstringandsponsor\.logo\.startswith\('http'\)elseurl_for\('static', filename='images/sponsors/'~\(sponsor\.logo or 'logo\.webp'\)\)\s*\}\}@{% if sponsor.logo and sponsor.logo.startswith('http') %}{{ sponsor.logo }}{% else %}{{ url_for('static', filename='images/sponsors/' ~ (sponsor.logo or 'logo.webp')) }}{% endif %}@g" \
  "$TEMPLATES_DIR/partials/sponsor_block.html"

echo "→ Converting HTML-encoded comparisons…"
find "$TEMPLATES_DIR/partials" -type f -name 'hero_and_fundraiser.html' -print0 \
  | xargs -0 sed -i -E 's/&gt;=/>=/g'

echo "→ Fixing quote_cite placeholders…"
sed -i -E \
  -e "s@\{\{\s*quote_citeifquote_citeelseurl_for\('main\.home'\)\s*\}\}@cite=\"{{ quote_cite if quote_cite else url_for('main.home') }}\"@g" \
  "$TEMPLATES_DIR/partials/hero_overlay_quote.html"

echo "→ Cleaning stray URL-encoding artifacts…"
find "$TEMPLATES_DIR" -type f -name '*.html' -print0 \
  | xargs -0 sed -i 's/%20//g'

echo "✅ Done! Templates patched. Backup at $BACKUP_DIR"
