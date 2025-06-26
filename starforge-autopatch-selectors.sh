#!/usr/bin/env bash
# starforge-autopatch-selectors.sh
set -e

echo "🏀 Starforge: Auto-patching missing JS/HTML id selectors…"
TEMPLATES_DIR="app/templates/"
JS_DIR="app/static/js/"

# 1. Gather all JS id selectors
ids=$(grep -rhoE "getElementById\(['\"]([^'\"]+)['\"]\)" $JS_DIR | sed -E "s/.*getElementById\(['\"]([^'\"]+)['\"]\).*/\1/" | sort | uniq)

for id in $ids; do
  # 2. See if it exists in HTML
  if ! grep -rq "id=\"$id\"" $TEMPLATES_DIR; then
    echo "❌ Missing id=\"$id\""
    # Try to suggest the likely target file (by JS filename or by id keyword)
    target=$(grep -ril "${id%-*}" $TEMPLATES_DIR | head -1)
    if [ -z "$target" ]; then
      target=$(find $TEMPLATES_DIR -type f -name "*.html" | head -1)
    fi
    echo "  > Most likely template: $target"
    echo "  > Example patch: <span id=\"$id\"></span>"
    read -p "    Patch $id into $target? (y/N): " answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
      # Add the id near the end, above </body> or last </div>
      if grep -q '</body>' "$target"; then
        sed -i "/<\/body>/i <span id=\"$id\" style=\"display:none\"></span>" "$target"
      else
        sed -i '$i <span id="'"$id"'" style="display:none"></span>' "$target"
      fi
      echo "    ✅ Patched!"
    else
      echo "    ⚠️  Skipped."
    fi
  else
    echo "✅ id=\"$id\" already exists."
  fi
done

echo "🏀 Starforge: Selector audit complete! Run your JS/UI and rerun checks for All-Star status."
