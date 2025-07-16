#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Starting auto-patch for Jinja syntax issues..."

templates=(
  "app/templates/base.html"
  "app/templates/index.html"
  "app/templates/become_sponsor.html"
  "app/templates/partials/header.html"
  "app/templates/partials/footer.html"
  "app/templates/partials/newsletter.html"
  "app/templates/partials/hero_and_fundraiser.html"
  "app/templates/partials/sponsor_block.html"
)

for file in "${templates[@]}"; do
  if [[ -f "$file" ]]; then
    timestamp=$(date +%s)
    backup="${file}.bak.$timestamp"
    echo "Backing up $file to $backup"
    cp "$file" "$backup"

    echo "Patching $file..."

    # Fix unescaped quotes inside attributes (convert double quotes inside attributes to single quotes)
    perl -pi -e '
      s/(=\s*"[^"]*?)"([^"]*?")/$1'\''$2/g;
    ' "$file"

    # Fix duplicate type attributes in buttons
    sed -i 's/\(<button[^>]*\) type="submit" type="button"/\1 type="submit"/g' "$file"
    sed -i 's/\(<button[^>]*\) type="button" type="submit"/\1 type="submit"/g' "$file"

    # Fix self-closing img tags that are malformed (remove trailing slashes inside Jinja blocks)
    sed -i 's/<img\s\([^>]*\)\s\/>/\<img \1\>/g' "$file"

    # Add src="" to img tags that lack src attribute (simplified)
    perl -pi -e '
      s{<img((?!src=)[^>]*)>}{"<img src=\"\"$1>"}g;
    ' "$file"

    # Remove spaces before closing Jinja tags
    sed -i 's/{% \+/{{/g' "$file"
    sed -i 's/ \+%}/%}}/g' "$file"

    # Fix broken Jinja blocks split across lines (join lines ending with {% and the next line)
    perl -0777 -pi -e 's/\{\%[ \t]*\n([^\}]+\%\})/\{% \1/g' "$file"

    echo "✅ Patched $file"
  else
    echo "⚠️ File not found: $file"
  fi
done

echo "🎉 Auto-patching complete! Review backups before deploying."
