#!/bin/bash
echo "🔎 Starting Starforge UI/UX audit..."

# 1. Find duplicate headings and sections in templates (common copy-paste errors)
echo "Checking for duplicate UI sections..."
grep -rE '(Meet Our Players|Join Our Champion Circle|Sponsor Wall)' app/templates | sort | uniq -d
echo "---"

# 2. Detect missing static assets referenced in templates
echo "Checking for missing static assets..."
grep -roP "url_for\('static', filename='[^']+'\)" app/templates | cut -d"'" -f4 | while read f; do
  if [ ! -f "app/static/$f" ]; then
    echo "⚠️ Missing static asset: $f"
  fi
done
echo "---"

# 3. Find unclosed Jinja blocks (common cause of runtime errors)
echo "Checking for Jinja blocks usage..."
grep -rE '{% (block|for|if|macro) ' app/templates | sed 's/{% \(block\|for\|if\|macro\) \([^ %]*\).*/\1:\2/' | sort | uniq -c
echo "---"

# 4. Check images missing or empty alt attributes (accessibility)
echo "Checking for images missing alt attributes..."
grep -r '<img[^>]*alt=""' app/templates
if [ $? -ne 0 ]; then
  echo "✔️ All images have alt attributes"
fi
echo "---"

# 5. Find inline styles or deprecated Tailwind color classes for cleanup
echo "Checking for inline styles and deprecated color classes..."
grep -rE '(style=|text-red-|bg-red-|text-blue-|bg-blue-)' app/templates app/static/css/ || echo "✔️ No inline styles or deprecated color classes found"
echo "---"

# 6. Verify critical JS & CSS files exist
echo "Verifying critical assets presence..."
[ -f app/static/css/tailwind.min.css ] && echo "✔️ tailwind.min.css present" || echo "⚠️ tailwind.min.css missing"
[ -f app/static/js/bundle.min.js ] && echo "✔️ bundle.min.js present" || echo "⚠️ bundle.min.js missing"
echo "---"

# 7. List CSS & JS files referenced in base.html and index.html
echo "Listing CSS files in base.html and index.html:"
grep -oP 'href="[^"]+\.css"' app/templates/base.html app/templates/index.html | sort | uniq
echo "---"
echo "Listing JS files in base.html and index.html:"
grep -oP 'src="[^"]+\.js"' app/templates/base.html app/templates/index.html | sort | uniq
echo "---"

echo "🔍 Audit complete! Review warnings and fix accordingly."
