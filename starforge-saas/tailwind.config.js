/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.{html,jinja,jinja2,j2,htm}",   // Scan all Jinja/HTML variants
    "./app/components/**/*.{html,jinja,jinja2,j2}",      // Optional: Component-style templates
    "./app/static/js/**/*.js",                           // Tailwind in Alpine/HTMX/JS
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: "#facc15", // Gold
        brand: "#fbbf24",   // Customizable brand accent
      },
    },
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    require("tailwindcss-animate"),
  ],
};

