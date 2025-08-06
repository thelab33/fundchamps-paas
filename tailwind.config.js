// tailwind.config.cjs
const plugin = require('tailwindcss/plugin');
const {
  zinc, yellow, black, white, red, blue, emerald, amber, indigo, orange, pink,
  transparent, sky, slate, gray, neutral, stone,
} = require('tailwindcss/colors');

// Safe loader so missing plugins never crash builds
const noop = plugin(() => {});
const safe = (name) => {
  try { return require(name); }
  catch { console.warn(`⚠️ Skipping optional plugin: ${name}`); return noop; }
};

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',

  content: [
    './app/templates/**/*.{html,jinja,jinja2}',
    './app/templates/partials/**/*.{html,jinja,jinja2}',
    './app/templates/macros/**/*.{html,jinja,jinja2}',
    './app/templates/admin/**/*.{html,jinja,jinja2}',
    './app/static/js/**/*.{js,ts}',
    './app/static/css/src/**/*.css',
    './app/**/*.py',
    './app/static/data/**/*.{json,txt}',
  ],

  safelist: [
    'bg-zinc-950', 'bg-zinc-900', 'bg-black', 'bg-yellow-400', 'text-yellow-400',
    'rounded-xl', 'rounded-2xl', 'sr-only',
    'shadow-gold-glow', 'shadow-xl-gold',
    { pattern: /^animate-(kenburns|bounce-in|fade-in|sparkle|shine|spin(-reverse-slow|-slow)?)$/ },
    {
      pattern:
        /^(from|via|to)-(yellow|zinc|black|white|amber|blue|red|emerald|indigo|orange|pink|sky|slate|gray|neutral|stone)-(50|100|200|300|400|500|600|700|800|900|950)(\/[0-9]{1,3})?$/
    },
    { pattern: /^(bg|text|border|ring|opacity|rounded|z|p[trblxy]?|m[trblxy]?|gap|font|tracking|h-|w-)/ },
    { pattern: /^z-\d+$/ },
    { pattern: /^z-\[\d+\]$/ },
  ],

  theme: {
    container: {
      center: true,
      padding: '1rem',
      screens: { sm: '640px', md: '768px', lg: '1024px', xl: '1280px', '2xl': '1440px' },
    },
    extend: {
      fontFamily: {
        sans: ['Inter', 'Montserrat', 'Roboto', 'Segoe UI', 'Arial', 'sans-serif'],
      },
      colors: {
        zinc, yellow, black, white, red, blue, emerald, amber, indigo, orange, pink,
        transparent, sky, slate, gray, neutral, stone,
        primary: '#facc15',
        'primary-gold': '#fbbf24',
        'primary-yellow': '#fde68a',
        'brand-black': '#09090b',
      },
      boxShadow: {
        'gold-glow': '0 0 8px 2px #facc15, 0 0 24px 0 #fde68a44',
        glass: '0 4px 32px 0 rgba(250,204,21,0.06), 0 1.5px 4.5px rgba(60,60,60,0.05)',
        'xl-gold': '0 20px 25px -5px rgba(250, 204, 21, 0.4), 0 10px 10px -5px rgba(250, 204, 21, 0.2)',
        'inner-glow': 'inset 0 0 15px #facc15cc',
      },
      keyframes: {
        kenburns: {
          '0%': { transform: 'scale(1.12) translateY(6px)', opacity: '0.94' },
          '100%': { transform: 'scale(1.01) translateY(0)', opacity: '1' },
        },
        'bounce-in': {
          '0%': { transform: 'scale(0.9) translateY(22px)', opacity: '0' },
          '70%': { transform: 'scale(1.08) translateY(-3px)', opacity: '1' },
          '100%': { transform: 'scale(1) translateY(0)', opacity: '1' },
        },
        shine: { '100%': { backgroundPosition: '200% center' } },
        sparkle: {
          '0%,100%': { opacity: '.8', transform: 'scale(1)' },
          '60%': { opacity: '1', transform: 'scale(1.28)' },
        },
        'fade-in': {
          '0%': { opacity: 0, transform: 'translateY(30px)' },
          '100%': { opacity: 1, transform: 'none' },
        },
      },
      animation: {
        kenburns: 'kenburns 18s ease-in-out infinite',
        'bounce-in': 'bounce-in 0.7s cubic-bezier(.22,1.61,.36,1) 1',
        shine: 'shine 2.1s linear infinite',
        sparkle: 'sparkle 1.3s ease-in-out infinite',
        'fade-in': 'fade-in 1.5s cubic-bezier(.39,.575,.565,1) both',
      },
      backgroundImage: {
        'gold-gradient': 'linear-gradient(90deg, #facc15 0%, #fbbf24 100%)',
        'amber-gradient': 'linear-gradient(45deg, #fbbf24 0%, #fde68a 100%)',
      },
      ringColor: { DEFAULT: '#facc15', 'primary-focus': '#fbbf24' },
      outline: { primary: ['2px solid #facc15', '4px'] },
      transitionProperty: {
        colors: 'color, background-color, border-color, text-decoration-color, fill, stroke',
        shadow: 'box-shadow',
        opacity: 'opacity',
      },
      transitionTimingFunction: { 'ease-in-out': 'cubic-bezier(0.4, 0, 0.2, 1)' },
      zIndex: { 99: '99', 999: '999', 9999: '9999', 99999: '99999' },
    },
  },

  plugins: [
    // Official plugins (loaded safely)
    safe('@tailwindcss/forms'),
    safe('@tailwindcss/typography'),
    safe('@tailwindcss/aspect-ratio'),
    safe('@tailwindcss/line-clamp'),

    // Animations: use community plugin (you installed it)
    safe('tailwindcss-animate'),

    // Elite UX utilities & variants
    plugin(function ({ addUtilities, addVariant, theme }) {
      addUtilities(
        {
          '.focus-ring-primary': {
            outline: `2px solid ${theme('colors.primary')}`,
            outlineOffset: '4px',
          },
          '.shadow-xl-gold': {
            boxShadow:
              '0 20px 25px -5px rgba(250, 204, 21, 0.4), 0 10px 10px -5px rgba(250, 204, 21, 0.2)',
          },
          '.transition-smooth': {
            transitionProperty:
              'color, background-color, border-color, text-decoration-color, fill, stroke, box-shadow, opacity',
            transitionDuration: '300ms',
            transitionTimingFunction: 'cubic-bezier(0.4, 0, 0.2, 1)',
          },
          '.bg-gold-gradient': { backgroundImage: theme('backgroundImage.gold-gradient') },
          '.bg-amber-gradient': { backgroundImage: theme('backgroundImage.amber-gradient') },
        },
        ['responsive', 'hover', 'focus', 'focus-visible']
      );

      addVariant('hocus', ['&:hover', '&:focus']);
      addVariant('supports-hover', '@media (hover: hover)');
      addVariant('aria-current', '&[aria-current="page"]');
      addVariant('aria-expanded', '&[aria-expanded="true"]');
      addVariant('aria-selected', '&[aria-selected="true"]');
      addVariant('data-open', '&[data-open="true"]');
      addVariant('data-active', '&[data-active="true"]');
    }),
  ],

  corePlugins: { preflight: true },

  future: {
    hoverOnlyWhenSupported: true,
    optimizeUniversalDefaults: true,
  },
};

