#!/bin/bash
set -e

BASE_DIR="app/static"
OLD_NESTED_DIR="$BASE_DIR/js/app/static"

echo "Starting static assets cleanup..."

# 1. Create target folders if missing
mkdir -p "$BASE_DIR/images" "$BASE_DIR/pay" "$BASE_DIR/videos" "$BASE_DIR/js/modules" "$BASE_DIR/board"

# 2. Move images (jpg, png, webp, svg) to images/ or pay/ or board/
echo "Moving images and SVGs..."
mv -v "$OLD_NESTED_DIR"/images/* "$BASE_DIR/images/" 2>/dev/null || true
mv -v "$OLD_NESTED_DIR"/pay/* "$BASE_DIR/pay/" 2>/dev/null || true
mv -v "$OLD_NESTED_DIR"/board/* "$BASE_DIR/board/" 2>/dev/null || true

# 3. Move videos (mp4, webm) to videos/
echo "Moving videos..."
mv -v "$OLD_NESTED_DIR"/*.mp4 "$BASE_DIR/videos/" 2>/dev/null || true

# 4. Move JS files from nested js/app/static to flat js/
echo "Flattening JS files..."
# Find all .js files under the nested js folder except assets, move to js/
find "$BASE_DIR/js/app/static" -type f -name '*.js' -exec mv -v {} "$BASE_DIR/js/" \; 2>/dev/null || true

# 5. Remove now empty nested folders (js/app/static etc.)
echo "Cleaning up empty folders..."
find "$BASE_DIR/js/app/static" -type d -empty -delete || true
find "$BASE_DIR/js/app" -type d -empty -delete || true

# 6. Fix static URL references in Jinja templates: change 'js/app/static/...' -> 'images/', 'pay/', 'videos/', or 'js/'
echo "Fixing static URLs in templates..."

# This is a basic bulk replacement for your main templates folder (adjust path if needed)
TEMPLATE_DIR="app/templates"

# Patterns to fix:
# - js/app/static/images/  -> images/
# - js/app/static/pay/     -> pay/
# - js/app/static/board/   -> board/
# - js/app/static/*.mp4    -> videos/
# - js/app/static/js/      -> js/

# Replace image paths
find "$TEMPLATE_DIR" -type f -name "*.html" -exec sed -i -E \
  -e 's#url_for\(\'static\', filename=\'js/app/static/images/#url_for(\'static\', filename=\'images/#g' \
  -e 's#url_for\(\'static\', filename=\'js/app/static/pay/#url_for(\'static\', filename=\'pay/#g' \
  -e 's#url_for\(\'static\', filename=\'js/app/static/board/#url_for(\'static\', filename=\'board/#g' \
  -e 's#url_for\(\'static\', filename=\'js/app/static/(.*\.mp4)#url_for(\'static\', filename=\'videos/\1#g' \
  -e 's#url_for\(\'static\', filename=\'js/app/static/js/#url_for(\'static\', filename=\'js/#g' \
  {} +

echo "✅ Static assets cleanup and template fixes complete!"

echo "👉 Remember to test your app and fix any remaining path issues manually if needed."
