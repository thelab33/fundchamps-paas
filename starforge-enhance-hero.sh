#!/usr/bin/env bash
# starforge-enhance-hero.sh — Instantly Supercharge Your Hero Section

set -e

STATIC_DIR="app/static"
TEMPLATES_DIR="app/templates"
JS_DIR="$STATIC_DIR/js"
CSS_DIR="$STATIC_DIR/css"

banner() {
  echo -e "\033[1;35m★ Starforge: Hero UI Enhancer ★\033[0m"
}

warn_missing() {
  [ ! -d "$1" ] && echo "⚠️  Missing $1 — creating it." && mkdir -p "$1"
}

inject_script_tag() {
  local script="$1"
  local template="${2:-$TEMPLATES_DIR/base.html}"
  # Only inject if not present
  grep -q "$script" "$template" || \
    sed -i "/<\/body>/i \\    <script src=\"{{ url_for('static', filename='js/$script') }}\"></script>" "$template"
}

banner

# 1. Stardust Sparkle Canvas + JS
warn_missing "$JS_DIR"
cat > "$JS_DIR/stardust.js" <<'EOF'
window.addEventListener('DOMContentLoaded',()=>{
  const c=document.getElementById('stardust-canvas');
  if(!c)return;
  c.width=c.offsetWidth; c.height=c.offsetHeight;
  const ctx=c.getContext('2d');
  const sparkles=Array.from({length:36},()=>({
    x:Math.random()*c.width,y:Math.random()*c.height,
    r:1+Math.random()*2, a:Math.random()*360, s:0.2+Math.random()*0.3
  }));
  function draw(){
    ctx.clearRect(0,0,c.width,c.height);
    sparkles.forEach(s=>{
      s.x+=Math.sin(s.a)*s.s;
      s.y+=Math.cos(s.a)*s.s;
      s.a+=0.02;
      if(s.x<0||s.x>c.width||s.y<0||s.y>c.height){
        s.x=Math.random()*c.width; s.y=Math.random()*c.height;
      }
      ctx.save();
      ctx.globalAlpha=0.38+0.4*Math.sin(s.a*1.3);
      ctx.beginPath();
      ctx.arc(s.x,s.y,s.r,0,2*Math.PI);
      ctx.fillStyle='#fde68a';
      ctx.shadowColor='#facc15';
      ctx.shadowBlur=6;
      ctx.fill();
      ctx.restore();
    });
    requestAnimationFrame(draw);
  }
  draw();
});
EOF

# 2. Hero Rotator Quotes
cat > "$JS_DIR/hero-rotator.js" <<'EOF'
window.addEventListener('DOMContentLoaded',()=>{
  const quotes=[
    "“Discipline creates leaders for life.” — Coach Angel",
    "🏆 92% of our seniors earned scholarships.",
    "✨ “Brotherhood first. Basketball second.”",
    "🚀 Join our journey—help us reach the championship!",
    "📚 Academics + Athletics = Champions"
  ];
  let i=0, el=document.getElementById('hero-rotator');
  function cycle(){
    if(el) {
      el.textContent=quotes[i];
      i=(i+1)%quotes.length;
    }
    setTimeout(cycle, 6000);
  }
  if(el) cycle();
});
EOF

# 3. Confetti Burst
cat > "$JS_DIR/confetti.js" <<'EOF'
window.addEventListener('DOMContentLoaded',()=>{
  let raised=document.getElementById('funds-raised-meter');
  let goal=document.getElementById('funds-goal-meter');
  if(raised && goal && parseFloat(raised.textContent) >= parseFloat(goal.textContent)){
    for(let i=0;i<80;i++){
      let c=document.createElement('div');
      c.className='confetti';
      c.style.left=Math.random()*100+'vw';
      c.style.backgroundColor=['#facc15','#fde68a','#b91c1c'][i%3];
      c.style.animationDelay=(Math.random()*0.9)+'s';
      document.body.appendChild(c);
      setTimeout(()=>c.remove(),1800);
    }
  }
});
EOF

# 4. Social Share Widget
cat > "$JS_DIR/share-widget.js" <<'EOF'
window.addEventListener('DOMContentLoaded',()=>{
  let b=document.getElementById('share-widget-btn');
  let p=document.getElementById('share-popup');
  if(b && p){
    b.onclick=()=>p.classList.toggle('hidden');
    // Click outside to close
    document.addEventListener('click',e=>{
      if(!b.contains(e.target) && !p.contains(e.target)) p.classList.add('hidden');
    });
  }
});
EOF

# 5. Add CSS for new effects if needed (can append to your tailwind/custom.css)
warn_missing "$CSS_DIR"
cat >> "$CSS_DIR/starforge-hero.css" <<'EOF'
/* Glow Border */
.animate-glow-border {
  border-radius: 1.5rem;
  border: 2.5px solid transparent;
  background: linear-gradient(90deg,#facc15,#fde68a,#b91c1c,#facc15);
  background-size: 400% 400%;
  animation: glow-border 3s infinite alternate, shimmer 8s linear infinite;
}
@keyframes glow-border {
  0% { box-shadow: 0 0 0 0 #facc15, 0 0 30px 8px #fde68a66;}
  50% { box-shadow: 0 0 0 2px #fde68a, 0 0 40px 20px #facc1580;}
  100% { box-shadow: 0 0 0 0 #facc15, 0 0 30px 8px #fde68a66;}
}
@keyframes shimmer {
  0% {background-position: 0% 50%;}
  100% {background-position: 100% 50%;}
}
/* Confetti */
.confetti {
  position: fixed; top: -2vh; width: 14px; height: 14px; border-radius: 50%;
  opacity: 0.88; pointer-events: none; z-index: 9999;
  animation: confetti-fall 1.8s cubic-bezier(.7,.1,.3,1.0) forwards;
}
@keyframes confetti-fall {
  0% { transform: translateY(-4vh) rotateZ(0deg) scale(1.2);}
  65% { opacity: 1;}
  100% { transform: translateY(120vh) rotateZ(1080deg) scale(1); opacity: 0;}
}
EOF

# 6. Inject <script> tags into your base template, if not already present
inject_script_tag "stardust.js"
inject_script_tag "hero-rotator.js"
inject_script_tag "confetti.js"
inject_script_tag "share-widget.js"

# 7. Alert for <canvas id="stardust-canvas"> in hero partial if not present
if !grep -q 'id="stardust-canvas"' $TEMPLATES_DIR/partials/hero_and_fundraiser.html; then
  echo "🔔 Reminder: Add <canvas id=\"stardust-canvas\" ...> to your hero partial for sparkles."
fi

# 8. Alert for #hero-rotator and #share-widget if not present
if !grep -q 'id="hero-rotator"' $TEMPLATES_DIR/partials/hero_and_fundraiser.html; then
  echo "🔔 Add <div id=\"hero-rotator\" ...> to your hero partial for rotating stats/quotes."
fi
if !grep -q 'id="share-widget"' $TEMPLATES_DIR/partials/hero_and_fundraiser.html; then
  echo "🔔 Add the share widget markup to your hero for social sharing."
fi

# 9. Remind to import starforge-hero.css in your CSS chain if using separate CSS
if !grep -q 'starforge-hero.css' "$TEMPLATES_DIR/base.html"; then
  echo "🔔 Remember to add <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/starforge-hero.css') }}\"> to your base.html head if not already included."
fi

echo -e "\n\033[1;32m✔️  Starforge Hero enhancements populated! Reload your page and enjoy.\033[0m"
