document.addEventListener("DOMContentLoaded", () => {
  console.log("⚡ Starforge JS initializing…");

  // Smooth scroll to top
  const backToTopBtn = document.getElementById("backToTop");
  backToTopBtn?.addEventListener("click", () =>
    window.scrollTo({ top: 0, behavior: "smooth" })
  );

  // Fade in headers (luxury reveal)
  const fadeHeaders = () => {
    document.querySelectorAll("h1, h2").forEach((el) => {
      if (!el.classList.contains("in-view") &&
          el.getBoundingClientRect().top < window.innerHeight - 60) {
        el.style.opacity = 1;
        el.classList.add("in-view");
      }
    });
  };
  document.querySelectorAll("h1, h2").forEach((el) => {
    el.style.opacity = 0;
    el.style.transition = "opacity 0.7s cubic-bezier(.4,0,.2,1)";
  });
  window.addEventListener("scroll", fadeHeaders);
  fadeHeaders();

  // Animate glass badges
  const badgeObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in-view");
        badgeObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.4 });
  document.querySelectorAll(".badge-glass").forEach((el) =>
    badgeObserver.observe(el)
  );

  // Fundraising meter animation
  function animateFundraiserMeter() {
    const bar = document.querySelector("#hero-meter-bar > div");
    const percentLabel = document.getElementById("hero-meter-percent");
    const emojiLabel = document.getElementById("emoji-milestone");
    const raised = parseFloat(document.getElementById("funds-raised")?.textContent.replace(/[^0-9.]/g, "") || "0");
    const goal = parseFloat(document.getElementById("funds-goal")?.textContent.replace(/[^0-9.]/g, "") || "1");
    if (bar && goal > 0) {
      const pct = Math.min((raised / goal) * 100, 100).toFixed(1);
      setTimeout(() => {
        bar.style.width = `${pct}%`;
        percentLabel.textContent = `${pct}%`;
        bar.setAttribute("aria-valuenow", raised);
        // Milestone emojis
        emojiLabel.textContent = pct >= 100 ? "🏆" : pct >= 75 ? "💪" : pct >= 50 ? "🔥" : pct >= 25 ? "🚀" : "💤";
      }, 350);
    }
  }
  animateFundraiserMeter();

  console.log("✅ Connect ATX Elite JavaScript loaded.");
});

// Sponsor Spotlight Modal (legacy, can be removed if you switch to toasts)
window.openSpotlight = function(sponsorName = "A Generous Donor") {
  document.getElementById('sponsor-name').innerHTML = `Thank you <span class="text-red-400 font-bold">${sponsorName}</span> for supporting the team!`;
  document.getElementById('sponsor-spotlight-modal').classList.add('show');
  if (typeof launchConfetti === "function") launchConfetti();
  setTimeout(closeSpotlight, 4000);
};
window.closeSpotlight = function() {
  document.getElementById('sponsor-spotlight-modal').classList.remove('show');
};

// SPONSOR LEADERBOARD (partial or live)
window.renderSponsorLeaderboard = function (sponsors = []) {
  const el = document.getElementById('sponsor-leaderboard-main');
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
// Example/test usage:
window.renderSponsorLeaderboard([
  { name: "Gold’s Gym", amount: 5000 },
  { name: "Rodriguez Law", amount: 2500 },
  { name: "Redline BBQ", amount: 1000 },
  { name: "Dr. White & Co.", amount: 500 },
]);

// SPONSOR ALERT (Championship Toast)
window.sponsorAlert = function(name, tier = "Champion Sponsor") {
  // Remove any existing alerts first!
  document.querySelectorAll('.starforge-sponsor-alert').forEach(e => e.remove());
  // Build the alert
  const div = document.createElement('div');
  div.className = "starforge-sponsor-alert fixed bottom-4 right-4 z-[9999] flex flex-col items-end animate-bounce-in";
  div.innerHTML = `
    <div class="bg-black border-4 border-gold rounded-2xl px-7 py-4 shadow-elevated flex flex-col items-center text-center">
      <img src="/static/images/logo.webp" class="w-12 h-12 mb-2 rounded-full border-2 border-gold shadow-gold-glow" alt="Logo" />
      <span class="text-lg font-bold text-gold mb-2">🔥 NEW SPONSOR ALERT! 🔥</span>
      <span class="text-white font-semibold mb-2">Thank you <b>${name}</b> for supporting the team!</span>
      <span class="prestige-badge">${tier} 🏆</span>
    </div>
  `;
  document.body.appendChild(div);
  setTimeout(() => div.remove(), 4800);
};
// Test it: window.sponsorAlert('Redline BBQ', 'Gold Sponsor');

// Confetti (optional)
// window.launchConfetti = function() { /* Add your confetti code here */ };

