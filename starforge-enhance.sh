#!/bin/bash

echo "🚀 Starforge Prestige Enhancement Initializing..."

# 1. Create luxury.css with glass badges
mkdir -p app/static/css && cat <<EOL > app/static/css/luxury.css
/* ✨ Luxury CSS Components */
.badge-glass {
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.08);
  color: #fff;
  backdrop-filter: blur(10px);
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.1);
}
.ring-gold-glow {
  @apply ring-4 ring-yellow-400 shadow-[0_0_12px_rgba(250,204,21,0.6)];
}
EOL

# 2. Modularize partial CSS
mkdir -p app/static/css/partials
mv app/static/css/{header,hero,footer,about,mission}.css app/static/css/partials/ 2>/dev/null || true

# 3. Add global variables
cat <<EOL > app/static/css/variables.css
:root {
  --primary: #facc15;
  --overlay-glass: rgba(18, 20, 34, 0.75);
  --text-light: #fff;
}
[data-theme='dark'] {
  --text-light: #e0e0e0;
}
EOL

# 4. Inject heading styles
cat <<EOL >> app/static/css/luxury.css

@layer base {
  h1, h2, h3 {
    @apply font-heading font-extrabold text-primary drop-shadow-lg tracking-tight;
  }
}
EOL

# 5. Add animation keyframes
cat <<EOL >> app/static/css/luxury.css

@keyframes slide-up {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}
.animate-slide-up {
  animation: slide-up 0.7s ease forwards;
}
EOL

# 6. Install AOS
npm install aos --save
echo "import 'aos/dist/aos.css';" >> app/static/js/main.js

# 7. Tailwind Purge + Rebuild
mkdir -p app/static/css/atomic
mv app/static/globals.css app/static/css/atomic/globals.css 2>/dev/null || true

npx tailwindcss -i ./app/static/css/atomic/globals.css -o ./app/static/tailwind.min.css --minify

# 8. Stylelint fix (if config exists)
npx stylelint "app/static/**/*.css" --fix 2>/dev/null || echo "⚠️ No stylelint config found."

echo "✨ Starforge Prestige Enhancement Complete. Project is now visually elite."
