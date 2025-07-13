#!/bin/bash
echo "🧹 Starforge CSS Purger — $(date)"

INPUT_CSS="app/static/css/globals.css"
UNUSED_CLASSES="reports/safe_to_purge_css_classes.txt"
BACKUP="backups/globals_$(date +%Y%m%d_%H%M%S).css"
PURGED="app/static/css/globals.purged.css"

# Backup original
cp "$INPUT_CSS" "$BACKUP"
echo "📦 Backup saved to $BACKUP"

# Check unused class list exists
if [[ ! -f "$UNUSED_CLASSES" ]]; then
  echo "❌ Unused class list not found: $UNUSED_CLASSES"
  echo "Please run the audit_css_ids.sh first."
  exit 1
fi

# Start purge
echo "🛠️ Purging unused CSS classes..."
cp "$INPUT_CSS" "$PURGED"

while read -r selector; do
  if [[ "$selector" == .* ]]; then
    clean_selector="${selector:1}"
    # Escape for regex
    safe_selector=$(echo "$clean_selector" | sed 's/[]\/$*.^|[]/\\&/g')
    # Comment out the whole block if found
    sed -i "/\.$safe_selector\s*{/,/}/s/^/\/\//" "$PURGED"
    echo "🗑️ Commented: .$clean_selector"
  fi
done < "$UNUSED_CLASSES"

echo "✅ Purge complete. Review $PURGED and delete comments when confirmed."
