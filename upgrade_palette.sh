#!/bin/bash
set -euo pipefail

echo "🚀 Starting Gold-to-Amber tone-down palette upgrade..."

# 1. Replace #facc15 with muted gold #d4af37
rg -l '#facc15' app/static/css | xargs -r sed -i 's/#facc15/#d4af37/g'

# 2. Replace #fde047 (hover gold) with #c99a2c
rg -l '#fde047' app/static/css | xargs -r sed -i 's/#fde047/#c99a2c/g'

# 3. Replace text-yellow-300 with text-yellow-400 (richer amber)
rg -l 'text-yellow-300' app/templates app/static/css | xargs -r sed -i 's/text-yellow-300/text-yellow-400/g'

# 4. Darken background gradient gold stops
rg -l 'from-yellow-400' app/static/css | xargs -r sed -i 's/from-yellow-400/from-yellow-500/g'
rg -l 'to-yellow-200' app/static/css | xargs -r sed -i 's/to-yellow-200/to-yellow-300/g'

# 5. Replace shadow-gold & #facc15 with shadow-amber-700 & #b8860b
rg -l 'shadow-gold' app/static/css | xargs -r sed -i 's/shadow-gold/shadow-amber-700/g'
rg -l '#facc15' app/static/css | xargs -r sed -i 's/#facc15/#b8860b/g'

# 6. Change ring-yellow-400 to ring-amber-600 in templates & CSS
rg -l 'ring-yellow-400' app/templates app/static/css | xargs -r sed -i 's/ring-yellow-400/ring-amber-600/g'

# 7. Replace bg-yellow-400 with amber gradient in templates & CSS
rg -l 'bg-yellow-400' app/templates app/static/css | xargs -r sed -i 's/bg-yellow-400/bg-gradient-to-r from-amber-500 to-amber-400/g'

# 8. Soften --focus-ring CSS variable to amber (#b8860b)
rg -l '--focus-ring' app/static/css | xargs -r sed -i 's/--focus-ring: var(--brand-gold)/--focus-ring: #b8860b/g'

# 9. Update pulse-glow animation glow color to amber
rg -l 'var(--focus-ring)' app/static/css | xargs -r sed -i 's/var(--focus-ring)/#b8860b/g'

# 10. Update confetti colors in JS from #facc15 to #b8860b
rg -l '#facc15' app/static/js | xargs -r sed -i 's/#facc15/#b8860b/g'

echo "✅ Palette upgrade complete! Run your CSS build to apply changes."

