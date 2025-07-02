#!/usr/bin/env bash
# starforge-enhance-quote.sh — Luxe Quote Power-Up for Connect ATX Elite

set -e

STATIC_DIR="app/static"
JS_DIR="$STATIC_DIR/js"
CSS_DIR="$STATIC_DIR/css"
PARTIAL="$STATIC_DIR/partials/hero_overlay_quote.html"
TEMPLATES_PARTIALS="app/templates/partials"
QUOTE_JS="$JS_DIR/overlay-quote.js"

banner() {
  echo -e "\033[1;35m★ Starforge: Hero Overlay Quote Luxe Enhancer ★\033[0m"
}

warn_missing() {
  [ ! -d "$1" ] && echo "⚠️  Missing $1 — creating it." && mkdir -p "$1"
}

banner

warn_missing "$JS_DIR"
warn_missing "$CSS_DIR"
warn_missing "$TEMPLATES_PARTIALS"

# 1. Update/Write JS for Copy Quote + Optional Animation
cat > "$QUOTE_JS" <<'EOF'
window.addEventListener('DOMContentLoaded',()=>{
  // Copy to clipboard handler
  const copyBtn = document.getElementById('copy-hero-quote');
  const quoteText = document.getElementById('hero-overlay-quote')?.querySelector('blockquote span');
  if (copyBtn && quoteText) {
    copyBtn.addEventListener('click',()=>{
      navigator.clipboard.writeText(quoteText.innerText.trim());
      copyBtn.textContent = 'Copied!';
      setTimeout(()=>copyBtn.textContent = 'Copy Quote', 1300);
    });
  }
  // (Optional) A11y: Focus figcaption on animation end for screen readers
  const fc = document.querySelector('#hero-overlay-quote figcaption');
  if(fc) fc.addEventListener('animationend',()=>fc.focus&&fc.focus());
});
EOF

# 2. Update/Write partial with Copy button (id=copy-hero-quote)
cat > "$TEMPLATES_PARTIALS/hero_overlay_quote.html" <<'EOF'
<figure
  id="hero-overlay-quote"
  class="absolute bottom-24 md:bottom-28 left-1/2 -translate-x-1/2 z-10 w-[92%] max-w-2xl px-4 rounded-2xl bg-black/70 border border-gold/70 backdrop-blur-lg shadow-xl animate-fade-in animate-delay-700 transition-transform duration-500 hover:scale-105"
  aria-label="Motivational quote"
  style="
    box-shadow:
      0 8px 32px rgba(250, 204, 21, 0.12),
      0 2px 12px rgba(0, 0, 0, 0.2);
  "
  itemscope
  itemtype="https://schema.org/Quotation"
>
  <blockquote
    class="relative text-white text-lg sm:text-xl font-semibold italic leading-relaxed drop-shadow-[0_2px_12px_rgba(0,0,0,.32)] px-2 md:px-8 py-5"
    cite="https://connectatxelite.com/coach"
    aria-live="polite"
    itemprop="text"
  >
    <svg class="absolute -left-2 -top-3 w-8 h-8 text-gold/70 opacity-80 select-none"
      fill="currentColor" viewBox="0 0 32 32" aria-hidden="true">
      <path d="M12 20a8 8 0 0 1 8-8V6A14 14 0 0 0 6 20v2a4 4 0 0 0 4 4h2a4 4 0 0 0 4-4z"/>
    </svg>
    <span class="block" style="text-shadow: 0 2px 12px rgba(0,0,0,0.32)">
      “The brotherhood and discipline we build here creates leaders for life.”
    </span>
    <svg class="absolute -right-2 -bottom-3 w-8 h-8 text-gold/70 opacity-80 select-none rotate-180"
      fill="currentColor" viewBox="0 0 32 32" aria-hidden="true">
      <path d="M12 20a8 8 0 0 1 8-8V6A14 14 0 0 0 6 20v2a4 4 0 0 0 4 4h2a4 4 0 0 0 4-4z"/>
    </svg>
  </blockquote>
  <figcaption
    class="mt-2 text-gold-light font-bold tracking-wide text-base flex items-center justify-center gap-1 animate-slide-up animate-delay-900"
    aria-label="Coach attribution"
    itemprop="author"
    itemscope
    itemtype="https://schema.org/Person"
    tabindex="0"
  >
    <span class="text-gold" itemprop="name">— Coach Angel Rodriguez</span>
    <svg class="w-5 h-5 text-gold animate-bounce" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <path d="M10 15l-5.5-5.5 1.4-1.4L10 12.2l4.1-4.1 1.4 1.4z" />
    </svg>
  </figcaption>
  <button
    id="copy-hero-quote"
    class="mt-2 ml-2 text-xs text-gold hover:text-gold-light bg-gold/10 rounded px-2 py-1 transition focus:outline-none focus-visible:ring-2 focus-visible:ring-yellow-300"
    type="button"
    aria-label="Copy motivational quote"
  >
    Copy Quote
  </button>
</figure>
EOF

# 3. Remind user to inject overlay quote partial and JS
BASE_TMPL="app/templates/base.html"
if ! grep -q 'overlay-quote.js' "$BASE_TMPL"; then
  sed -i "/<\/body>/i \\    <script src=\"{{ url_for('static', filename='js/overlay-quote.js') }}\"></script>" "$BASE_TMPL"
  echo "🔗 Injected overlay-quote.js into $BASE_TMPL"
fi

echo -e "\n\033[1;32m✔️  Starforge Luxe Overlay Quote powered up! Make sure {% include \"partials/hero_overlay_quote.html\" %} is present in your hero section.\033[0m"
