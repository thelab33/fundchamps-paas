# Save as: starforge-polish-css.sh, then run: bash starforge-polish-css.sh

CSS="app/static/css/globals.css"
BACKUP="${CSS}.bak.$(date +%s)"

set -e

echo "🔒 Backing up $CSS → $BACKUP"
cp "$CSS" "$BACKUP"

echo "🚦 Auditing for unused custom properties:"
for var in $(grep -oP 'var\(--\K[a-zA-Z0-9\-]+' "$CSS" | sort | uniq); do
  grep -r --color "$var" app/templates app/static/js > /dev/null || echo "❌ $var UNUSED"
done

echo "🔗 Ensuring Google Fonts @import..."
grep -q Montserrat "$CSS" || sed -i '1i@import url("https://fonts.googleapis.com/css2?family=Montserrat:wght@700;900&family=Roboto:wght@400;700&display=swap");' "$CSS"

echo "✨ Adding font-smoothing to html if missing..."
grep -q 'font-smoothing' "$CSS" || sed -i '/^html {/a\  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;' "$CSS"

echo "🎨 Adding background-size to heading gradients/buttons (shine effects)..."
awk '/\.heading-gradient/ && !/background-size/ {print; print "  background-size: 400% 100%;"; next} 1' "$CSS" | sponge "$CSS"
awk '/\.btn-glow::before/ && !/background-size/ {print; print "  background-size: 400% 100%;"; next} 1' "$CSS" | sponge "$CSS"

echo "🧹 Removing unused button classes (btn-primary/secondary/glow)..."
for c in btn-primary btn-secondary btn-glow; do
  grep -rq "$c" app/templates app/static/js || sed -i "/\.$c\s*{/,/}/d" "$CSS"
done

echo "🎯 Running Prettier/Stylelint auto-fix (optional polish)..."
command -v stylelint > /dev/null && npx stylelint --fix "$CSS" || true
command -v prettier > /dev/null && npx prettier --write "$CSS" || true

echo "📊 Brand color summary (for your review):"
grep -oE '#[0-9a-fA-F]{3,6}|var\(--[a-z0-9\-]+\)' "$CSS" | sort | uniq -c | sort -nr

echo "🎬 Animation/keyframes found:"
awk '/@keyframes/{print; k=1; next} k&&/}/ {print; k=0; next} k{print}' "$CSS"

echo "✅ $CSS is now Starforge-polished! (Backup at $BACKUP)"
echo "Ready for launch! 🚀"
