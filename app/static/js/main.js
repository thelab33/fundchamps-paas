// Starforge Elite — main.js (Production-Ready, Real-Time Fundraising)

document.addEventListener("DOMContentLoaded", () => {
  console.log("⚡ Starforge JS initializing…");

  // ---- 1. Real-Time Socket.IO Integration ----
  // Make sure socket.io.js is loaded!
  let socket;
  try {
    socket = io(); // Defaults to current origin
  } catch (e) {
    console.warn("⚠️ Socket.IO not available! Real-time features disabled.");
  }

  // --- Real-Time Events ---
  if (socket) {
    // 1. Show live ticker on every donation
    socket.on("new_donation", (data) => {
      showDonationTicker(
        `🎉 <b>$${data.amount.toLocaleString()}</b> from <b>${escapeHTML(
          data.name
        )}</b> – Thank you!`
      );
      if (typeof window.launchConfetti === "function") window.launchConfetti();
    });

    // 2. Show sponsor spotlight modal/alert
    socket.on("new_sponsor", (data) => {
      window.sponsorAlert(data.name, "Champion Sponsor");
      window.openSpotlight(data.name);
      // Optionally re-render leaderboard (pull via AJAX if needed)
      // fetchSponsorsAndUpdateLeaderboard();
    });

    // 3. (Flex) Update leaderboard, badges, etc.
    socket.on("vip_update", (data) => {
      // TODO: implement VIP badge or leaderboard live update
    });
  }

  // ---- 2. Smooth Scroll to Top ----
  const backToTopBtn = document.getElementById("backToTop");
  if (backToTopBtn) {
    backToTopBtn.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" })
    );
  }

  // ---- 3. Luxury Header/Headline Reveal ----
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

  // ---- 4. Glass Badge/Prestige Micro-interactions ----
  if ("IntersectionObserver" in window) {
    const badgeObserver = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("in-view");
            entry.target.classList.add("animate-sparkle");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.4 }
    );
    document
      .querySelectorAll(".badge-glass, .prestige-badge")
      .forEach((el) => badgeObserver.observe(el));
  }

  // ---- 5. Fundraiser Meter Animation ----
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
      raisedEl.textContent.replace(/[^0-9.]/g, "") || "0"
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

  // ---- 6. A11y Toast Example ----
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

  // ---- 7. Mobile Menu Toggle + Focus Trap ----
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

  // ---- 8. Confetti + Haptic (if available) ----
  window.launchConfetti = function () {
    if (window.navigator.vibrate) window.navigator.vibrate([22, 16, 6]);
    // If using canvas-confetti, trigger here:
    // if (window.confetti) window.confetti({ particleCount: 120, spread: 84, origin: { y: 0.65 } });
  };

  // ---- 9. Alpine.js/htmx events (future flex) ----
  document.addEventListener("alpine:init", () => {
    // Alpine.data('admin', () => ({}));
  });

  // ---- 10. Ready log ----
  console.log("✅ Connect ATX Elite JavaScript loaded.");
});

/*-----------------------------
  Live Donation Ticker (A11y, Upgrades)
------------------------------*/
window.showDonationTicker = function (msg) {
  let ticker = document.getElementById("donation-ticker");
  if (!ticker) {
    ticker = document.createElement("div");
    ticker.id = "donation-ticker";
    ticker.className =
      "fixed bottom-8 left-1/2 -translate-x-1/2 bg-yellow-400/95 text-black font-bold px-7 py-3 rounded-2xl shadow-xl z-[9999] animate-bounce-in text-lg";
    ticker.setAttribute("role", "status");
    ticker.setAttribute("aria-live", "polite");
    document.body.appendChild(ticker);
  }
  ticker.innerHTML = msg;
  ticker.classList.add("show");
  setTimeout(() => ticker.classList.remove("show"), 4000);
};

/*-----------------------------
  Sponsor Spotlight Modal
------------------------------*/
window.openSpotlight = function (sponsorName = "A Generous Donor") {
  const modal =
    document.getElementById("sponsor-spotlight-modal") ||
    document.getElementById("sponsor-spotlight-modal-footer");
  const nameEl =
    document.getElementById("sponsor-name") ||
    document.getElementById("sponsor-name-footer");
  if (!modal || !nameEl) return;
  nameEl.innerHTML = `<span class="text-red-400 font-bold">${escapeHTML(
    sponsorName
  )}</span>`;
  modal.classList.add("show");
  modal.setAttribute("aria-modal", "true");
  if (typeof window.launchConfetti === "function") window.launchConfetti();
  setTimeout(window.closeSpotlight, 4000);
};
window.closeSpotlight = function () {
  const modal =
    document.getElementById("sponsor-spotlight-modal") ||
    document.getElementById("sponsor-spotlight-modal-footer");
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
        }">${escapeHTML(s.name)}</span>
        <span class="text-xl font-bold mt-2 ${
          i === 0 ? "text-red-400" : "text-white/60"
        }">$${s.amount.toLocaleString()}</span>
        ${i === 0 ? '<div class="prestige-badge mt-3">🏆 Top Champion</div>' : ""}
      </div>
    `
    )
    .join("");
};

// Demo/test example (remove in prod):
// window.renderSponsorLeaderboard([
//   { name: "Gold’s Gym", amount: 5000 },
//   { name: "Rodriguez Law", amount: 2500 },
//   { name: "Redline BBQ", amount: 1000 },
//   { name: "Dr. White & Co.", amount: 500 },
// ]);

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
      <span class="text-white font-semibold mb-2">Thank you <b>${escapeHTML(
        name
      )}</b> for supporting the team!</span>
      <span class="prestige-badge">${tier} 🏆</span>
    </div>
  `;
  document.body.appendChild(div);
  setTimeout(() => div.remove(), 4800);
};

/*-----------------------------
  Utility: Escape HTML for Security
------------------------------*/
function escapeHTML(str) {
  return (str + "")
    .replace(/[&<>"']/g, function (m) {
      return (
        {
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        }[m] || m
      );
    });
}


// --- confetti.js ---
export function launchConfetti() {
  const colors = ["#facc15", "#dc2626", "#fff", "#18181b"];
  for (let i = 0; i < 64; i++) {
    const confetti = document.createElement("div");
    confetti.className = "confetti";
    confetti.style.background =
      colors[Math.floor(Math.random() * colors.length)];
    confetti.style.left = `${Math.random() * 100}vw`;
    confetti.style.animationDelay = `${Math.random() * 1.5}s`;
    document.body.appendChild(confetti);
    setTimeout(() => confetti.remove(), 1800);
  }
}


// --- quotes.js ---
const quotes = [
  {
    text: "The brotherhood and discipline we build here creates leaders for life.",
    author: "Coach A. Rodriguez",
    title: "Program Director",
    avatar: "/static/images/coach-avatar.jpg",
  },
  {
    text: "We’re not just coaching basketball. We’re shaping futures.",
    author: "Coach Jasmine",
    title: "Academic Coordinator",
    avatar: "/static/images/coach2.jpg",
  },
  {
    text: "This team changed my life — it gave me purpose, focus, and family.",
    author: "Jordan M.",
    title: "Alumni Captain",
    avatar: "/static/images/player1.jpg",
  },
];
let currentQuoteIndex = 0;
function showQuote(i) {
  const q = quotes[i];
  document.getElementById("hero-quote-text").innerText = q.text;
  document.getElementById("hero-quote-author").innerText = q.author;
  document.getElementById("hero-quote-title").innerText = q.title;
  document.getElementById("hero-quote-avatar").src = q.avatar;
}
function showNextQuote() {
  currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
  showQuote(currentQuoteIndex);
}
function showPrevQuote() {
  currentQuoteIndex = (currentQuoteIndex - 1 + quotes.length) % quotes.length;
  showQuote(currentQuoteIndex);
}
function copyQuote() {
  const q = quotes[currentQuoteIndex];
  navigator.clipboard.writeText(`"${q.text}" — ${q.author}, ${q.title}`);
  alert("Quote copied!");
}
function shareQuote() {
  const q = quotes[currentQuoteIndex];
  if (navigator.share)
    navigator.share({
      title: "Connect ATX Elite",
      text: `"${q.text}" — ${q.author}`,
    });
  else alert("Share not supported.");
}
document.addEventListener("DOMContentLoaded", () => showQuote(0));
