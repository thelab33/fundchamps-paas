#!/bin/bash

echo "🧼 Starforge CSS & ID Usage Audit — $(date)"
mkdir -p reports

# 1. Extract all classes & IDs used in HTML (Jinja included)
echo "🔎 Extracting classes and IDs from HTML..."
grep -rhoP '(class|id)="[^"]+"' app/templates | \
  sed -E 's/(class|id)="([^"]+)"/\2/' | \
  tr ' ' '\n' | \
  sort | uniq > reports/html_selectors.txt

# 2. Extract all class & ID names from Tailwind/CSS (exact matches)
echo "🔎 Extracting selectors from CSS..."
grep -oP '\.[a-zA-Z0-9_-]+' app/static/css/*.css | sed 's/^\.//' | sort | uniq > reports/css_classes.txt
grep -oP '#[a-zA-Z0-9_-]+' app/static/css/*.css | sed 's/^#//' | sort | uniq > reports/css_ids.txt

# 3. Detect unused CSS classes/IDs
echo "🚫 CSS classes not used in HTML:"
comm -23 reports/css_classes.txt reports/html_selectors.txt > reports/unused_css_classes.txt
echo "🚫 CSS IDs not used in HTML:"
comm -23 reports/css_ids.txt reports/html_selectors.txt > reports/unused_css_ids.txt

# 4. Detect HTML classes/IDs that are not defined in CSS
echo "🚫 HTML selectors missing from CSS:"
comm -13 reports/css_classes.txt reports/html_selectors.txt > reports/html_classes_not_in_css.txt

echo "✅ Audit complete. Check reports/ for:"
echo " - unused_css_classes.txt"
echo " - unused_css_ids.txt"
echo " - html_classes_not_in_css.txt"
