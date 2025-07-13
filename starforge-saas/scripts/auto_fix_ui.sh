#!/bin/bash
echo "🔧 Starforge UI Auto-Fix Script — $(date)"

BACKUP_DIR="backups/starforge_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 1. Add type="button" to <button> elements missing it
echo "🧼 Fixing <button> elements without type..."
find app/templates -name '*.html' | while read -r file; do
  grep -q '<button[^>]*>' "$file" || continue
  cp "$file" "$BACKUP_DIR/"
  sed -i 's/<button\([^>]*\)\([^t][^y][^p][^e][^=]*\)>/<button\1 type="button"\2>/g' "$file"
done

# 2. Add loading="lazy" and decoding="async" to <img> tags
echo "📷 Enhancing <img> performance..."
find app/templates -name '*.html' | while read -r file; do
  grep -q '<img[^>]*>' "$file" || continue
  cp "$file" "$BACKUP_DIR/"
  sed -i 's/<img\(.*\)>/<img\1 loading="lazy" decoding="async">/g' "$file"
done

# 3. Touch missing static asset files
if [[ -f reports/missing_images.txt ]]; then
  echo "📂 Creating placeholder files for missing assets..."
  grep 'MISSING:' reports/missing_images.txt | cut -d' ' -f2- | while read -r path; do
    fullpath=$(echo "$path" | sed 's|^.*static/|app/static/|')
    mkdir -p "$(dirname "$fullpath")"
    touch "$fullpath"
    echo "📁 Touched: $fullpath"
  done
else
  echo "⚠️ No missing_images.txt found. Skipping asset patching."
fi

echo "✅ Auto-fix complete. Backups saved to $BACKUP_DIR"
