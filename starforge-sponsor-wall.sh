#!/bin/bash
# starforge-sponsor-wall.sh

set -e

echo "🏆 Starforge: Installing Sponsor Wall…"

# 1. Inject Sponsor Wall section partial (call this from a page or modal)
cat > app/templates/partials/sponsor_wall.html <<'EOW'
<section id="sponsor-wall" class="py-10 md:py-16 relative bg-gradient-to-b from-black via-secondary to-black/90">
  <div class="container mx-auto max-w-3xl px-4 flex flex-col items-center">
    <h2 class="text-3xl md:text-5xl font-black heading-gradient mb-6 flex items-center gap-3">
      <span>🏆</span>Sponsor Wall
      <span class="prestige-badge ml-2">2024</span>
    </h2>
    <p class="mb-8 text-lg text-white/80 max-w-xl text-center">
      Fueling dreams—thanks to every sponsor who supports our youth on and off the court!
    </p>
    <div id="sponsor-leaderboard" class="w-full grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
      <!-- Sponsor cards injected by JS -->
    </div>
    <button onclick="document.getElementById('become-sponsor-modal').classList.add('show')" class="btn-primary btn-glow text-xl px-8 py-3 mt-2 shadow-inner-gold uppercase tracking-wider">
      Become a Sponsor
    </button>
  </div>
</section>

<!-- Sponsor Modal (simple version, expand as needed) -->
<div id="become-sponsor-modal" class="fixed inset-0 z-[1000] bg-black/60 flex items-center justify-center opacity-0 pointer-events-none transition-all duration-300">
  <div class="bg-gradient-to-br from-gold via-black to-red-700 rounded-2xl p-8 max-w-md w-full flex flex-col items-center shadow-elevated relative">
    <button onclick="document.getElementById('become-sponsor-modal').classList.remove('show')" class="absolute top-3 right-3 text-2xl text-gold hover:text-red-500">&times;</button>
    <h3 class="text-2xl font-bold text-gold mb-2">Become a Sponsor</h3>
    <p class="mb-4 text-white/80">Leave your mark—help us reach the championship!</p>
    <form>
      <input type="text" placeholder="Your Name / Company" class="w-full mb-3 px-4 py-2 rounded bg-black/60 text-white border border-gold/30 focus:outline-none focus:ring-2 focus:ring-gold" />
      <input type="number" placeholder="Sponsorship Amount" class="w-full mb-3 px-4 py-2 rounded bg-black/60 text-white border border-gold/30 focus:outline-none focus:ring-2 focus:ring-gold" />
      <button type="submit" class="btn-primary btn-glow w-full">Sponsor Now</button>
    </form>
  </div>
</div>
EOW

# 2. Add show modal class
echo '#become-sponsor-modal.show { opacity: 1 !important; pointer-events: auto !important; }' >> app/static/css/globals.css

# 3. Add dynamic JS for loading sponsors (add/merge to your main.js)
cat >> app/static/js/main.js <<'EOM'

window.renderSponsorLeaderboard = function (sponsors = []) {
  const el = document.getElementById('sponsor-leaderboard');
  if (!el) return;
  if (sponsors.length === 0) {
    el.innerHTML = `<div class="col-span-2 text-center text-lg text-gold/80 font-semibold">Be our first sponsor! 🏅</div>`;
    return;
  }
  el.innerHTML = sponsors
    .map(
      (s, i) => `
      <div class="rounded-2xl border-4 ${i === 0 ? 'border-gold bg-gradient-to-r from-gold/20 via-red-700/10 to-white/10 scale-105 shadow-inner-gold animate-pulse' : 'border-white/20 bg-black/40'} shadow-elevated p-5 flex flex-col items-center text-center">
        <span class="text-2xl font-extrabold ${i === 0 ? 'text-gold drop-shadow' : 'text-white/80'}">${s.name}</span>
        <span class="text-xl font-bold mt-2 ${i === 0 ? 'text-red-400' : 'text-white/60'}">$${s.amount.toLocaleString()}</span>
        ${i === 0 ? '<div class="prestige-badge mt-3">🏆 Top Champion</div>' : ''}
      </div>
    `
    )
    .join('');
};

// Example usage (replace this with your live data source / fetch API call)
window.renderSponsorLeaderboard([
  { name: "Gold’s Gym", amount: 5000 },
  { name: "Rodriguez Law", amount: 2500 },
  { name: "Redline BBQ", amount: 1000 },
  { name: "Dr. White & Co.", amount: 500 },
]);

EOM

echo "🏆 Sponsor Wall: Partial injected, JS leaderboard ready, modal live!"
echo "• Call {% include 'partials/sponsor_wall.html' %} where you want it."
echo "• Rebuild assets: npm run build"
echo "• Add live data/fetch to window.renderSponsorLeaderboard() for real sponsors."
echo "🚩 Want leaderboard API wiring? Just say: Starforge: Leaderboard API next!"

# End of script
