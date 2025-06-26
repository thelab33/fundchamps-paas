/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  safelist: [
    'btn-glow',
    'btn-primary',
    'btn-secondary',
    'text-gradient',
    'heading-gradient',
    'shadow-inner-gold',
    'shadow-elevated',
    'shadow-ambient',
    'border-animated',
    'prestige-badge',
    'before:absolute',
    'before:inset-0',
    'before:bg-gradient-to-r',
    'before:from-yellow-400',
    'before:via-yellow-200',
    'before:to-yellow-400',
    'before:opacity-10',
    'before:z-[-1]',
  ],
  theme: {
    extend: {
      colors: {
        // Brand/core palette
        gold: "#facc15",
        red: "#b91c1c",         // Deeper, bolder red for championship energy
        black: "#18181b",
        white: "#fff",
        blue: {
          DEFAULT: "#0a1f44",   // Signature blue
          dark: "#061633",      // Optional: deeper blue
        },

        // Semantic naming for easy swapping in @apply/utilities
        primary: "#facc15",       // Gold is primary!
        secondary: "#0a1f44",     // Blue is secondary
        neutral: "#18181b",       // Deep black for backgrounds

        // Extra for gradients or fine-tuning
        "red-light": "#f87171",
        "red-dark": "#7f1d1d",
        "gold-light": "#fde68a",
        "gold-dark": "#bca004",
      },
      animation: {
        shine: "shine 2.5s linear infinite",
        "border-glint": "border-glint 2.5s ease-in-out infinite",
      },
      keyframes: {
        shine: {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
        "border-glint": {
          "0%": { borderColor: "#facc15" },
          "50%": { borderColor: "#fde68a" },
          "100%": { borderColor: "#facc15" },
        },
      },
    },
  },
  darkMode: "class",
  plugins: [],
};

