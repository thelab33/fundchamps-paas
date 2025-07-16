/** @type {import('tailwindcss').Config} */
module.exports = {
  // Enable dark mode toggle via adding 'class' to <html> or <body>
  darkMode: "class",

  // Paths to all templates and JS/CSS files where Tailwind classes might appear
  content: [
    "./app/templates/**/*.{html,jinja2}",  // HTML + Jinja2 templates
    "./app/static/**/*.{js,css}",         // JS and CSS for dynamic classes
  ],

  // Safelist: Keep classes even if they're not used in the content files
  safelist: [
    {
      pattern:
        /^(animate|bg|text|hover:bg|hover:text|focus:ring|border|ring|shadow|scale|opacity|translate|pointer-events|grid-cols|flex|hidden|block|rounded|p|m|gap|font|uppercase|tracking|shadow)-/,
    },
    // Explicit classes used dynamically or via JS/templates that must never purge
    "bg-zinc-900",
    "text-primary",
    "bg-primary-yellow",
    "font-bold",
    "rounded-xl",
    "shadow-gold-glow",
    "text-white/90",
    "animate-bounce-in",
    "animate-delay-700",
    "animate-delay-900",
    "animate-fade-in-up",
    "animate-kenburns",
    "animate-marquee",
    "animate-pop",
    "animate-sparkle",
    "animate-spin-reverse-slow",
    "animate-spin-slow",
  ],

  // Extend the default Tailwind theme
  theme: {
    extend: {
      fontFamily: {
        roboto: ['"Roboto"', "Arial", "sans-serif"],
        montserrat: ['"Montserrat"', '"Roboto"', "Arial", "sans-serif"],
      },
      colors: {
        primary: "#facc15",              // Yellow primary color
        "primary-yellow": "#fde68a",     // Lighter yellow for highlighting
        red: "#b91c1c",                  // Red accent color
        blue: "#0a1f44",                 // Dark blue for accents
        black: "#18181b",                // Black base
        white: "#ffffff",                // White
        zinc: {
          900: "#18181b",                // Darker shade of zinc for text and backgrounds
          800: "#27272a",                // Lighter shade of zinc for accents
        },
      },
      animation: {
        "shine-move": "shine-move 2.8s linear infinite",        // Smooth shine animation
        "fade-in-up": "fadeInUp 0.7s ease forwards",           // Fade-in-up animation
        kenburns: "kenburns 20s ease infinite",                  // Ken Burns animation
        marquee: "marquee 25s linear infinite",                  // Marquee effect
        pop: "pop 0.3s ease forwards",                           // Pop effect
        sparkle: "sparkle 1.8s ease-in-out infinite",            // Sparkling effect
        "spin-reverse-slow": "spin-reverse 5s linear infinite",  // Slow reverse spin
        "spin-slow": "spin 7s linear infinite",                  // Slow spin animation
      },
      keyframes: {
        "shine-move": {
          "0%": { "background-position": "200% 0" },
          "100%": { "background-position": "-200% 0" },
        },
        fadeInUp: {
          "0%": { opacity: 0, transform: "translateY(15px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
        kenburns: {
          "0%": { transform: "scale(1.1) translate(0, 0)" },
          "100%": { transform: "scale(1) translate(-20px, -20px)" },
        },
        marquee: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-100%)" },
        },
        pop: {
          "0%": { transform: "scale(0.86)" },
          "100%": { transform: "scale(1)" },
        },
        sparkle: {
          "0%, 100%": { opacity: 0.6, transform: "translateY(0)" },
          "50%": { opacity: 1, transform: "translateY(-3px)" },
        },
        spin: {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(360deg)" },
        },
        "spin-reverse": {
          "0%": { transform: "rotate(0deg)" },
          "100%": { transform: "rotate(-360deg)" },
        },
      },
    },
  },

  // Plugins to add utility features
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/line-clamp"),
  ],

  // Enable corePlugins
  corePlugins: {
    preflight: true,   // Enables Tailwind's CSS reset
  },

  // Enable future-proof features
  future: {
    hoverOnlyWhenSupported: true,  // Optimized hover styles
    optimizeUniversalDefaults: true, // Improved default optimizations
  },
};

