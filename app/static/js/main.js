// Starforge Elite — main.js (Elevated)
document.addEventListener("DOMContentLoaded", () => {
  console.log("⚡ Starforge JS initializing…");

  // 1. Smooth Scroll to Top
  const backToTopBtn = document.getElementById("backToTop");
  if (backToTopBtn) {
    backToTopBtn.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" }),
    );
  }

  // 2. Luxury Header/Headline Reveal with rAF Throttle
  let ticking = false;
  function fadeHeaders() {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        document.querySelectorAll("h1, h2").forEach((el) => {
          if (
            !el.classList.contains("in-view") &&
            el.getBoundingClientRect().top < window.innerHeight - 60
          ) {
            el.style.opacity = 1;
            el.classList.add("in-view");
          }
        });
        ticking = false;
      });
      ticking = true;
    }
  }
  document.querySelectorAll("h1, h2").forEach((el) => {
    el.style.opacity = 0;
    el.style.transition = "opacity 0.7s cubic-bezier(.4,0,.2,1)";
  });
  window.addEventListener("scroll", fadeHeaders, { passive: true });
  fadeHeaders();

  // 3. Glass Badge/Prestige Micro-interactions
  if ("IntersectionObserver" in window) {
    const badgeObserver = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            // Optional: micro-sparkle effect
            entry.target.classList.add("animate-sparkle");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 },
    );
    document
      .querySelectorAll(".badge-glass, .prestige-badge")
      .forEach((el) => badgeObserver.observe(el));
  }

  // 4. Fundraiser Meter Animation + Accessible Emoji
  function animateFundraiserMeter() {
    const bar = document.querySelector("#hero-meter-bar > div, .progress-bar");
    const percentLabel = document.getElementById("hero-meter-percent");
    const emojiLabel = document.getElementById("emoji-milestone");
    const raisedEl =
      document.getElementById("funds-raised") ||
      document.getElementById("funds-raised-meter");
    const goalEl =
      document.getElementById("funds-goal") ||
      document.getElementById("funds-goal-meter");
    if (!bar || !raisedEl || !goalEl) return;
    const raised = parseFloat(
      raisedEl.textContent.replace(/[^0-9.]/g, "") || "0",
    );
    const goal = parseFloat(goalEl.textContent.replace(/[^0-9.]/g, "") || "1");
    const pct = Math.min((raised / goal) * 100, 100).toFixed(1);
    setTimeout(() => {
      bar.style.width = `${pct}%`;
      if (percentLabel) percentLabel.textContent = `${pct}%`;
      if (emojiLabel)
        emojiLabel.textContent =
          pct >= 100
            ? "🏆"
            : pct >= 75
              ? "💪"
              : pct >= 50
                ? "🔥"
                : pct >= 25
                  ? "🚀"
                  : "💤";
      bar.setAttribute("aria-valuenow", raised);
    }, 350);
  }
  animateFundraiserMeter();

  // 5. A11y Toast Example
  const toast = document.getElementById("vip-toast");
  if (toast && !sessionStorage.getItem("vipToastShown")) {
    toast.textContent =
      "🎉 Welcome! New sponsors will be spotlighted here — you could be next!";
    toast.classList.remove("hidden");
    toast.setAttribute("role", "status");
    toast.setAttribute("aria-live", "polite");
    setTimeout(() => toast.classList.add("hidden"), 6500);
    sessionStorage.setItem("vipToastShown", "1");
  }

  // 6. Mobile Menu Toggle + Focus Trap (Bonus)
  const hamburger = document.getElementById("hamburger");
  const mobileMenu = document.getElementById("mobile-menu");
  if (hamburger && mobileMenu) {
    hamburger.addEventListener("click", () => {
      const open = mobileMenu.classList.toggle("open");
      hamburger.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) {
        mobileMenu.querySelector("a,button,input")?.focus();
        document.body.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "";
      }
    });
  }

  // 7. Confetti + Haptic (if available)
  window.launchConfetti = function () {
    if (window.navigator.vibrate) window.navigator.vibrate([22, 16, 6]);
    // (insert confetti animation logic here, or use CanvasConfetti for pro)
    // Example: confetti({
    //   particleCount: 120, spread: 84, origin: { y: 0.65 }
    // });
  };

  // 8. Alpine.js or htmx events for admin/future dynamic UX
  document.addEventListener("alpine:init", () => {
    // Alpine.data('admin', () => ({}));
  });

  // 9. Ready log
  console.log("✅ Connect ATX Elite JavaScript loaded.");
});

/*-----------------------------
  Sponsor Spotlight Modal
------------------------------*/
window.openSpotlight = function (sponsorName = "A Generous Donor") {
  const modal = document.getElementById("sponsor-spotlight-modal");
  const nameEl = document.getElementById("sponsor-name");
  if (!modal || !nameEl) return;
  nameEl.innerHTML = `Thank you <span class="text-red-400 font-bold">${sponsorName}</span> for supporting the team!`;
  modal.classList.add("show");
  modal.setAttribute("aria-modal", "true");
  if (typeof window.launchConfetti === "function") window.launchConfetti();
  setTimeout(window.closeSpotlight, 4000);
};
window.closeSpotlight = function () {
  const modal = document.getElementById("sponsor-spotlight-modal");
  if (modal) modal.classList.remove("show");
};

/*-----------------------------
  Sponsor Leaderboard (Dynamic)
------------------------------*/
window.renderSponsorLeaderboard = function (sponsors = []) {
  const el = document.getElementById("sponsor-leaderboard-main");
  if (!el) return;
  if (sponsors.length === 0) {
    el.innerHTML = `<div class="col-span-2 text-center text-lg text-gold/80 font-semibold">Be our first sponsor! 🏅</div>`;
    return;
  }
  el.innerHTML = sponsors
    .map(
      (s, i) => `
      <div class="rounded-2xl border-4 ${
        i === 0
          ? "border-gold bg-gradient-to-r from-gold/20 via-red-700/10 to-white/10 scale-105 shadow-inner-gold animate-pulse"
          : "border-white/20 bg-black/40"
      } shadow-elevated p-5 flex flex-col items-center text-center">
        <span class="text-2xl font-extrabold ${
          i === 0 ? "text-gold drop-shadow" : "text-white/80"
        }">${s.name}</span>
        <span class="text-xl font-bold mt-2 ${
          i === 0 ? "text-red-400" : "text-white/60"
        }">$${s.amount.toLocaleString()}</span>
        ${i === 0 ? '<div class="prestige-badge mt-3">🏆 Top Champion</div>' : ""}
      </div>
    `,
    )
    .join("");
};

// Demo/test example:
window.renderSponsorLeaderboard([
  { name: "Gold’s Gym", amount: 5000 },
  { name: "Rodriguez Law", amount: 2500 },
  { name: "Redline BBQ", amount: 1000 },
  { name: "Dr. White & Co.", amount: 500 },
]);

/*-----------------------------
  Sponsor Alert (Championship Toast)
------------------------------*/
window.sponsorAlert = function (name, tier = "Champion Sponsor") {
  document
    .querySelectorAll(".starforge-sponsor-alert")
    .forEach((e) => e.remove());
  const div = document.createElement("div");
  div.className =
    "starforge-sponsor-alert fixed bottom-4 right-4 z-[9999] flex flex-col items-end animate-bounce-in";
  div.setAttribute("role", "status");
  div.setAttribute("aria-live", "polite");
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

// Starforge: Unstoppable production UI! Add new UX magic here.
