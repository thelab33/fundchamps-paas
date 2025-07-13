#!/usr/bin/env bash
set -euo pipefail

TPL="app/templates/partials/sponsor_block.html"
BACKUP=".backup/sponsor_block_$(date +%Y%m%d_%H%M%S).html"

echo "→ Backing up $TPL → $BACKUP"
mkdir -p "$(dirname "$BACKUP")"
cp "$TPL" "$BACKUP"

echo "→ Patching sponsor logo placeholder…"
sed -i -E '
  s@\{\{\s*sponsor\.logoifsponsor\.logo\.isstringandsponsor\.logo\.startswith\('"'"'http'"'"'\)elseurl_for\('"'"'static'"'"', filename='"'"'images/sponsors/'"'"'~\(sponsor\.logo or '"'"'logo\.webp'"'"'\)\)\s*\}\}@\
{% if sponsor.logo and sponsor.logo.startswith("http") %}\
  <img src="{{ sponsor.logo }}" alt="{{ sponsor.name }}" class="w-24 h-auto"/>\
{% else %}\
  <img src="{{ url_for("static", filename="images/sponsors/" ~ (sponsor.logo or "logo.webp")) }}" alt="{{ sponsor.name }}" class="w-24 h-auto"/>\
{% endif %}@g
' "$TPL"

echo "✅ sponsor_block.html patched. Backup at $BACKUP"
