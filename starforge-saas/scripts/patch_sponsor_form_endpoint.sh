#!/usr/bin/env bash
set -euo pipefail

TPL="app/templates/partials/sponsor_block.html"
BACKUP=".backup/$(basename "$TPL")_$(date +%Y%m%d_%H%M%S).html"

echo "→ Backing up $TPL to $BACKUP"
mkdir -p "$(dirname "$BACKUP")"
cp "$TPL" "$BACKUP"

echo "→ Updating form action endpoint…"
# If you want to post to the WTForms route, point to main.sponsor instead of the old become_sponsor
sed -i \
  -e "s|url_for('main.become_sponsor')|url_for('main.sponsor')|g" \
  "$TPL"

echo "✅ sponsor_block.html patched. Original at $BACKUP"
