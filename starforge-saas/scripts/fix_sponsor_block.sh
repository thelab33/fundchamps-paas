#!/usr/bin/env bash
set -euo pipefail

TPL="app/templates/partials/sponsor_block.html"
BACKUP=".backup/$(basename "$TPL")_$(date +%Y%m%d_%H%M%S).html"

echo "→ Backing up $TPL → $BACKUP"
mkdir -p "$(dirname "$BACKUP")"
cp "$TPL" "$BACKUP"

echo "→ Removing broken one-liners…"
sed -i '/sponsor\.logoifsponsor/d' "$TPL"

echo "→ Injecting proper Jinja logo block…"
awk '
  # Look for the start of each sponsor item
  /<div[^>]*class=".*sponsor-item.*">/ {
    print
    # Inject our logo snippet immediately after
    print "  <div class=\"sponsor-logo mb-4\">"
    print "    {% if sponsor.logo and sponsor.logo.startswith(\"http\") %}"
    print "      <img src=\"{{ sponsor.logo }}\""
    print "           alt=\"{{ sponsor.name }}\""
    print "           loading=\"lazy\""
    print "           class=\"w-24 h-auto mx-auto rounded-lg shadow-md\" />"
    print "    {% else %}"
    print "      <img src=\"{{ url_for('static', filename='images/sponsors/' ~ (sponsor.logo or 'logo.webp')) }}\""
    print "           alt=\"{{ sponsor.name }}\""
    print "           loading=\"lazy\""
    print "           class=\"w-24 h-auto mx-auto rounded-lg shadow-md\" />"
    print "    {% endif %}"
    print "  </div>"
    next
  }
  { print }
' "$TPL" > "${TPL}.patched" && mv "${TPL}.patched" "$TPL"

echo "✅ sponsor_block.html is now clean (original backed up at $BACKUP)"
