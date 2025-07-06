module.exports = {
  darkMode: "class",
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
    "./app/static/css/**/*.css"
  ],
  safelist: [
    "bg-zinc-900", // add other dynamic classes you use here
    "text-primary",
    "bg-primary-yellow",
    "font-bold",
    "rounded-xl",
    "shadow-gold-glow"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#facc15",
        "primary-yellow": "#facc15",
        zinc: {
          900: "#18181b"
        }
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/animation")
  ]
};

