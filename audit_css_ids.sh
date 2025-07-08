#!/bin/bash
echo "🔍 Starting CSS class and ID audit..."

TAILWIND_CSS="app/static/css/tailwind.min.css"
TEMPLATES_DIR="app/templates"
JS_DIR="app/static/js"

# 1. Extract all CSS classes from templates (class="...") and flatten to single words
echo "Extracting CSS classes used in templates..."
grep -rhoP 'class="[^"]+"' "$TEMPLATES_DIR" | sed 's/class=//g' | tr -d '"' | tr ' ' '\n' | sort -u > /tmp/used_classes.txt

# 2. Extract all CSS classes from tailwind.min.css
echo "Extracting CSS classes from Tailwind CSS build..."
grep -oP '\.[a-z0-9-_:/()]+(?=[\s,{])' "$TAILWIND_CSS" | sed 's/^\.//' | sort -u > /tmp/defined_classes.txt

# 3. Find classes used but NOT defined (possible typos or missing config)
echo "Classes used in templates but missing in Tailwind CSS:"
comm -23 /tmp/used_classes.txt /tmp/defined_classes.txt || echo "✔️ No missing CSS classes found"
echo "---"

# 4. Extract all IDs from templates and JS (id="...")
echo "Extracting all IDs from templates and JS..."
grep -rhoP 'id="[^"]+"' "$TEMPLATES_DIR" "$JS_DIR" | sed 's/id=//g' | tr -d '"' | sort > /tmp/all_ids.txt

# 5. Find duplicate IDs (should be unique in HTML)
echo "Checking for duplicate IDs..."
sort /tmp/all_ids.txt | uniq -d > /tmp/duplicate_ids.txt
if [ -s /tmp/duplicate_ids.txt ]; then
  echo "⚠️ Duplicate IDs found:"
  cat /tmp/duplicate_ids.txt
else
  echo "✔️ No duplicate IDs found."
fi
echo "---"

# 6. Verify IDs referenced in JS are declared in HTML/templates (basic check)
echo "Verifying IDs referenced in JS exist in templates..."
JS_IDS=$(grep -rhoP "getElementById\(['\"]([^'\"]+)['\"]\)" "$JS_DIR" | sed -E "s/getElementById\(['\"]([^'\"]+)['\"]\)/\1/" | sort -u)
MISSING_IDS=""
for id in $JS_IDS; do
  if ! grep -q "id=\"$id\"" "$TEMPLATES_DIR"/*; then
    MISSING_IDS="$MISSING_IDS $id"
  fi
done
if [ -n "$MISSING_IDS" ]; then
  echo "⚠️ IDs referenced in JS but not found in templates: $MISSING_IDS"
else
  echo "✔️ All IDs referenced in JS found in templates."
fi
echo "---"

echo "✅ CSS class and ID audit complete!"
