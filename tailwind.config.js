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
        primary: "#facc15",
        secondary: "#18181b",
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

