#!/usr/bin/env bash
# scripts/fix_if_elseurl_for.sh — Patch malformed if…elseurl_for placeholders
set -euo pipefail

echo "→ Patching malformed if…elseurl_for placeholders in templates…"
find app/templates -type f -name '*.html' -print0 \
  | xargs -0 sed -E -i \
      -e "s#\{\{\s*([a-zA-Z0-9_]+)if\1elseurl_for\('([^']+)'\)\s*\}\}#{{ \1 if \1 else url_for('\2') }}#g"

echo "✅ Done! Now restart your server:"
echo "   flask run --reload"
