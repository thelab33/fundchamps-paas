#!/bin/bash
# starforge-championship-mode.sh

set -e

echo "🏆 Starforge: Activating Championship Mode for Connect ATX Elite..."

# 1. Add confetti JS
cat > app/static/js/confetti.js <<'EOC'
export function launchConfetti() {
  const colors = ["#facc15", "#dc2626", "#fff", "#18181b"];
  for (let i = 0; i < 64; i++) {
    const confetti = document.createElement("div");
    confetti.className = "confetti";
    confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
    confetti.style.left = `${Math.random() * 100}vw`;
    confetti.style.animationDelay = `${Math.random() * 1.5}s`;
    document.body.appendChild(confetti);
    setTimeout(() => confetti.remove(), 1800);
  }
}
EOC

# 2. Add confetti CSS to globals
cat >> app/static/css/globals.css <<'EOC'

/* --- Championship Confetti --- */
.confetti {
  position: fixed;
  top: -2vh;
  width: 14px;
  height: 14px;
  border-radius: 30% 70% 60% 40% / 60% 40% 70% 30%;
  opacity: 0.88;
  pointer-events: none;
  z-index: 9999;
  animation: confetti-fall 1.8s cubic-bezier(.7,.1,.3,1.0) forwards;
}
@keyframes confetti-fall {
  0% { transform: translateY(-4vh) rotateZ(0deg) scale(1.2);}
  90% { opacity: 0.99;}
  100% { transform: translateY(110vh) rotateZ(720deg) scale(1); opacity: 0;}
}
EOC

# 3. Add Sponsor Spotlight Modal to footer
cat >> app/templates/partials/footer.html <<'EOM'

<!-- Sponsor Spotlight Modal -->
<div id="sponsor-spotlight-modal" class="fixed inset-0 z-[1000] flex items-center justify-center bg-black/70 backdrop-blur-sm transition-opacity opacity-0 pointer-events-none duration-300">
  <div class="bg-gradient-to-br from-black via-red-900/90 to-gold rounded-3xl shadow-ambient border-4 border-gold max-w-lg w-full p-10 flex flex-col items-center text-center relative animate-pulse">
    <button onclick="closeSpotlight()" class="absolute top-4 right-4 text-gold hover:text-red-500 text-3xl font-bold leading-none">&times;</button>
    <img src="/static/images/logo.webp" alt="Logo" class="w-16 h-16 rounded-full shadow-inner-gold ring-2 ring-gold mb-4">
    <h2 class="text-3xl font-extrabold text-gold mb-3">🔥 NEW SPONSOR ALERT! 🔥</h2>
    <p class="text-xl text-white mb-4" id="sponsor-name">Thank you <span class="text-red-400 font-bold">[Sponsor Name]</span> for supporting the team!</p>
    <div class="prestige-badge bg-gold text-black font-bold px-6 py-2 mt-2 border border-white/20 shadow-inner-gold">
      🏆 Champion Sponsor!
    </div>
  </div>
</div>
EOM

# 4. Add modal show class to CSS
echo '#sponsor-spotlight-modal.show { opacity: 1 !important; pointer-events: auto !important; }' >> app/static/css/globals.css

# 5. Inject JS for modal control into main.js if not already present
grep -q 'openSpotlight' app/static/js/main.js || cat >> app/static/js/main.js <<'EOF'

import { launchConfetti } from './confetti.js';

window.openSpotlight = function(sponsorName = "A Generous Donor") {
  document.getElementById('sponsor-name').innerHTML = `Thank you <span class="text-red-400 font-bold">${sponsorName}</span> for supporting the team!`;
  document.getElementById('sponsor-spotlight-modal').classList.add('show');
  if (typeof launchConfetti === "function") launchConfetti();
  setTimeout(closeSpotlight, 4000);
};
window.closeSpotlight = function() {
  document.getElementById('sponsor-spotlight-modal').classList.remove('show');
};
EOF

# 6. Add championship hero stripes
cat >> app/templates/partials/hero.html <<'EOH'
<div class="absolute left-0 top-16 w-full h-24 pointer-events-none select-none z-0 flex flex-row gap-3 opacity-60">
  <div class="flex-1 bg-gradient-to-r from-red-600 via-gold/80 to-white rounded-r-full blur-xl"></div>
  <div class="flex-1 bg-gradient-to-l from-gold via-black to-red-600 rounded-l-full blur-xl"></div>
</div>
EOH

# 7. Patch Tailwind config with championship palette (manual for reliability)
sed -i '/extend: {/a \
      colors: {\
        gold: "#facc15",\
        red: "#dc2626",\
        black: "#18181b",\
        white: "#fff",\
        primary: "#facc15",\
        secondary: "#18181b",\
      },' tailwind.config.js

echo "🏆 Starforge: Championship Mode is live!"
echo "• Confetti ready"
echo "• Sponsor modal injected"
echo "• Hero stripes loaded"
echo "• Tailwind colors set: red, white, black, gold"
echo "• Main JS is patched"
echo "🚀 Rebuild assets: npm run build"
echo "🌟 You’re in Championship Mode! #WinTheDay"

# End of script
