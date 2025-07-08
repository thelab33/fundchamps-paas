module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  safelist: [
    {
      pattern: /^(animate|bg|text|hover:bg|hover:text|focus:ring|border|ring|shadow|scale|opacity|translate|pointer-events|grid-cols|flex|hidden|block|rounded|p|m|gap|font|uppercase|tracking|shadow)-/,
    },
    "animate-bounce-in",
    "animate-delay-700",
    "animate-delay-900",
    "animate-fadeInUp",
    "animate-kenburns",
    "animate-marquee",
    "animate-pop",
    "animate-sparkle",
    "animate-spin-reverse-slow",
    "animate-spin-slow",
  ],
  theme: {
    extend: {
      // your existing extensions
    },
  },
  plugins: [],
};
