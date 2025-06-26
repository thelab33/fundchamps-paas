document.addEventListener("DOMContentLoaded", () => {
  console.log("⚡ Starforge JS initializing…");

  // Scroll-to-top button
  const backToTopBtn = document.getElementById("backToTop");
  backToTopBtn?.addEventListener("click", () =>
    window.scrollTo({ top: 0, behavior: "smooth" })
  );

  // Fade-in headers on scroll
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

  // Animate badge-glass elements on scroll
  const badgeObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("in-view");
        badgeObserver.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.4,
  });

  document.querySelectorAll(".badge-glass").forEach((el) =>
    badgeObserver.observe(el)
  );

  // ✅ Animate fundraising meter
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

        // 🎉 Emoji milestones
        if (pct >= 100) emojiLabel.textContent = "🏆";
        else if (pct >= 75) emojiLabel.textContent = "💪";
        else if (pct >= 50) emojiLabel.textContent = "🔥";
        else if (pct >= 25) emojiLabel.textContent = "🚀";
        else emojiLabel.textContent = "💤";
      }, 350);
    }
  }

  animateFundraiserMeter();

  console.log("✅ Connect ATX Elite JavaScript loaded.");
});

