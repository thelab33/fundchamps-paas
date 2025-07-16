#!/bin/bash
set -euo pipefail

FILE="app/templates/partials/sponsor_block.html"
BACKUP="${FILE}.bak.$(date +%s)"

echo "Backing up original file to $BACKUP"
cp "$FILE" "$BACKUP"

echo "Patching malformed <img> tags in $FILE ..."

# Step 1: Fix empty or missing src attributes by adding fallback src using Jinja2 default
sed -i -E '
  # Match <img src= with missing or empty src and replace with fallback
  s#<img\s+src=(["'\'']?)\s*["'\'']?( [^>]*)?#<img src="{{ sponsor.logo_url if sponsor.logo_url else url_for('\''static'\'', filename='\''images/default-sponsor-logo.png'\'') }}"\2#g
' "$FILE"

# Step 2: Ensure all <img> tags have alt attribute; if missing add alt="{{ sponsor.name }} logo"
# This adds alt attribute only if none present
sed -i -E '
  /<img / {
    /alt=/! s#(<img [^>]*)>#\1 alt="{{ sponsor.name }} logo" loading="lazy" decoding="async">#
  }
' "$FILE"

echo "Patch applied successfully to $FILE"
echo "Backup saved at $BACKUP"
