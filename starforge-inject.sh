#!/bin/bash
# ░█▀█░█▀█░█▀█░▀█▀░█▀▀░█▀▄░█▀▀░█░█
# ░█▄█░█▀▄░█▀█░░█░░█▀▀░█▀▄░█░░░█▀█
# ░▀░▀░▀░▀░▀░▀░░▀░░▀▀▀░▀░▀░▀▀▀░▀░▀
# Starforge Inject: Connect ATX Elite Edition

echo "🚀 Starforge injecting luxury components into Connect ATX Elite..."

partials="app/templates/partials"
static_css="app/static/css"
static_js="app/static/js"

mkdir -p "$partials" "$static_css" "$static_js"

# 1. Replace header.html
cat > "$partials/header.html" <<'EOF'
<!-- ✨ Elevated Header Partial -->
<header class="sticky top-0 z-50 w-full bg-secondary/90 backdrop-blur-md shadow-xl border-b border-primary/30 transition-all">
  <div class="container mx-auto flex items-center justify-between px-4 py-4 lg:px-8">
    <a href="{{ url_for('main.home') }}" class="flex items-center gap-3 focus-visible:ring-4 focus-visible:ring-amber-400 rounded-2xl outline-none">
      <img src="{{ url_for('static', filename='images/logo.webp') }}" alt="Connect ATX Elite logo" class="h-12 w-12 rounded-full ring-4 ring-yellow-400 shadow-gold-glow" />
      <span class="text-2xl font-extrabold tracking-tight text-primary animate-shine drop-shadow-lg">Connect ATX Elite</span>
    </a>
    <nav class="hidden lg:flex items-center gap-8 font-medium text-foreground" aria-label="Primary Navigation">
      <a href="{{ url_for('main.home') }}" class="hover:text-primary transition">Home</a>
      <a href="#about" class="hover:text-primary transition">About</a>
      <a href="#contact" class="hover:text-primary transition">Contact</a>
    </nav>
  </div>
</header>
EOF

# 2. Replace hero.html
cat > "$partials/hero.html" <<'EOF'
<!-- ✨ Elevated Hero Section -->
<section id="hero" class="connect-hero relative z-20 flex flex-col justify-center items-center min-h-[92vh] md:min-h-screen overflow-hidden" aria-labelledby="hero-heading" tabindex="-1">
  <div class="absolute inset-0 z-0 overflow-hidden pointer-events-none">
    <img src="{{ url_for('static', filename='images/connect-atx-team.jpg') }}" alt="Team huddle" class="w-full h-full object-cover opacity-95 scale-105 animate-kenburns" />
    <div class="absolute inset-0 bg-[var(--overlay-glass)]"></div>
  </div>
  {% include "partials/fundraiser_meter.html" %}
  <div class="container mx-auto max-w-3xl text-center z-20 px-4 py-16 flex flex-col items-center">
    <img src="{{ url_for('static', filename='images/logo.webp') }}" alt="Connect ATX Elite logo" class="w-32 h-32 mb-6 drop-shadow-xl rounded-full border-4 border-yellow-300 bg-white/80 animate-fade-in" />
    {% if current_user is defined and current_user.is_authenticated %}
    <div class="inline-flex items-center gap-2 mb-4 bg-gradient-to-r from-yellow-400 to-yellow-200 text-zinc-900 px-5 py-2 rounded-xl shadow animate-shine">Welcome, {{ current_user.name.split()[0] }} <span class="ml-2 animate-sparkle">✨</span></div>
    {% endif %}
    <h1 id="hero-heading" class="text-5xl sm:text-6xl font-extrabold mb-4 tracking-tight text-white drop-shadow-xl animate-slide-up">Connect ATX Elite</h1>
    <p class="text-lg sm:text-xl text-zinc-100/90 max-w-xl mx-auto mb-8 animate-slide-up delay-100">Empowering Youth Through Basketball, Brotherhood & Academics</p>
    <a href="#tiers" class="bg-yellow-400 hover:bg-yellow-300 font-bold py-3 px-8 rounded-full shadow-lg transition animate-pop delay-200">Become a Sponsor</a>
    <div class="mt-6 font-semibold text-white animate-fade-in delay-300">💰 <span class="text-yellow-300 font-bold">${{ raised }}</span> raised of <span class="text-yellow-300 font-bold">${{ goal }}</span></div>
    <div class="flex flex-wrap justify-center gap-4 mt-8 animate-fade-in delay-500">
      <span class="badge-glass">🏅 Trusted by 500+ Families</span>
      <span class="badge-glass">📚 Top 1% Academic Athletes</span>
      <span class="badge-glass">🏀 AAU Gold Certified</span>
    </div>
  </div>
  <button id="scroll-hint" class="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce" aria-label="Scroll down">
    <svg class="w-8 h-8 text-yellow-400 drop-shadow" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7"/></svg>
  </button>
  {% include "partials/hero_overlay_quote.html" %}
</section>
EOF

# 3. Replace hero_overlay_quote.html
cat > "$partials/hero_overlay_quote.html" <<'EOF'
<!-- ✨ Hero Overlay Quote Glass Card -->
<div class="hero-quote-glass backdrop-blur-md bg-black/40 rounded-3xl shadow-2xl p-6 max-w-2xl mx-auto mt-8 text-white relative animate-fade-in">
  <div class="hero-quote-arrows absolute top-4 right-4 flex gap-2">
    <button class="text-xl font-bold text-yellow-400 hover:scale-110 transition" onclick="showPrevQuote()">←</button>
    <button class="text-xl font-bold text-yellow-400 hover:scale-110 transition" onclick="showNextQuote()">→</button>
  </div>
  <blockquote id="hero-quote-text" class="text-lg italic text-center">Loading inspirational quotes…</blockquote>
  <div class="mt-4 flex items-center justify-center gap-3">
    <img id="hero-quote-avatar" src="" class="h-10 w-10 rounded-full ring-2 ring-yellow-300" alt="Coach avatar" />
    <div>
      <span id="hero-quote-author" class="block font-bold text-yellow-300">Coach</span>
      <span id="hero-quote-title" class="text-xs text-zinc-300">Title</span>
    </div>
  </div>
  <div class="mt-4 flex justify-center gap-4">
    <button onclick="copyQuote()" class="px-4 py-2 rounded-full bg-yellow-400 text-black font-semibold shadow hover:bg-yellow-300">Copy</button>
    <button onclick="shareQuote()" class="px-4 py-2 rounded-full bg-yellow-400 text-black font-semibold shadow hover:bg-yellow-300">Share</button>
  </div>
</div>
EOF

# 4. Replace footer.html
cat > "$partials/footer.html" <<'EOF'
<!-- ✨ Elevated Footer -->
<footer class="mt-16 py-8 text-center text-sm text-zinc-400 relative border-t border-primary/30 bg-gradient-to-t from-black via-zinc-900 to-transparent overflow-hidden">
  <div class="absolute inset-0 opacity-5 pointer-events-none bg-center bg-no-repeat bg-contain" style="background-image: url('{{ url_for('static', filename='images/logo.webp') }}');"></div>
  <p>&copy; {{ 2024 }} Connect ATX Elite — All rights reserved.</p>
</footer>
EOF

# 5. Create elevated.css
cat > "$static_css/elevated.css" <<'EOF'
/* ✨ CSS Utilities from Starforge Upgrade */
@keyframes kenburns { from { transform: scale(1.05); } to { transform: scale(1.12) translate(-5%, -5%); } }
@keyframes shine { 0% { background-position: -200%; } 100% { background-position: 200%; } }
@keyframes badge-in { from { opacity: 0; transform: translateY(20px) scale(0.95); } to { opacity: 1; transform: translateY(0) scale(1); } }
@keyframes pulse-cta { 0% { transform: scale(1); box-shadow: 0 0 0 0 #facc15; } 70% { transform: scale(1.05); box-shadow: 0 0 0 12px transparent; } 100% { transform: scale(1); box-shadow: 0 0 0 0 transparent; } }
@keyframes fade-in { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: none; } }
@keyframes slide-up { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
@keyframes pop { 0% { transform: scale(0.95); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

.animate-kenburns { animation: kenburns 22s ease-in-out infinite alternate; }
.animate-shine { background: linear-gradient(90deg, #facc15, #fde68a, #facc15); background-size: 300%; -webkit-background-clip: text; -webkit-text-fill-color: transparent; animation: shine 3s linear infinite; }
.animate-slide-up { animation: slide-up 0.9s ease-out forwards; }
.animate-fade-in { animation: fade-in 0.8s ease-out forwards; }
.animate-pop { animation: pop 0.6s ease-out forwards; }
.shadow-gold-glow { box-shadow: 0 0 12px rgba(250, 204, 21, 0.5); }
.badge-glass { opacity: 0; background: rgba(0, 0, 0, 0.3); padding: 0.5rem 1rem; border-radius: 1rem; border: 1px solid #facc15; color: white; font-weight: 500; animation: badge-in 1s forwards; }
EOF

# 6. Create quotes.js
cat > "$static_js/quotes.js" <<'EOF'
const quotes = [
  { text: "The brotherhood and discipline we build here creates leaders for life.", author: "Coach A. Rodriguez", title: "Program Director", avatar: "/static/images/coach-avatar.jpg" },
  { text: "We’re not just coaching basketball. We’re shaping futures.", author: "Coach Jasmine", title: "Academic Coordinator", avatar: "/static/images/coach2.jpg" },
  { text: "This team changed my life — it gave me purpose, focus, and family.", author: "Jordan M.", title: "Alumni Captain", avatar: "/static/images/player1.jpg" }
];
let currentQuoteIndex = 0;
function showQuote(i) { const q = quotes[i]; document.getElementById("hero-quote-text").innerText = q.text; document.getElementById("hero-quote-author").innerText = q.author; document.getElementById("hero-quote-title").innerText = q.title; document.getElementById("hero-quote-avatar").src = q.avatar; }
function showNextQuote() { currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length; showQuote(currentQuoteIndex); }
function showPrevQuote() { currentQuoteIndex = (currentQuoteIndex - 1 + quotes.length) % quotes.length; showQuote(currentQuoteIndex); }
function copyQuote() { const q = quotes[currentQuoteIndex]; navigator.clipboard.writeText(`"${q.text}" — ${q.author}, ${q.title}`); alert("Quote copied!"); }
function shareQuote() { const q = quotes[currentQuoteIndex]; if (navigator.share) navigator.share({ title: "Connect ATX Elite", text: `"${q.text}" — ${q.author}` }); else alert("Share not supported."); }
document.addEventListener("DOMContentLoaded", () => showQuote(0));
EOF

echo "✅ Starforge inject complete. All partials, CSS, and JS are now live."
