/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/**/*.html',
    './app/static/js/**/*.js',
  ],

  // classes you generate dynamically (e.g. via JS) but must ship
  safelist: [
    'btn-glow','btn-primary','btn-secondary',
    'text-gradient','heading-gradient',
    'shadow-inner-gold','shadow-elevated','shadow-ambient',
    'border-animated','prestige-badge',
    // before/after utilities for glow cards
    'before:absolute','before:inset-0',
    'before:bg-gradient-to-r','before:from-yellow-400',
    'before:via-yellow-200','before:to-yellow-400',
    'before:opacity-10','before:z-[-1]',
  ],

  darkMode: 'class',

  theme: {
    container: {
      center: true,
      padding: '1rem',
      screens: {
        xs: '420px',
        ...require('tailwindcss/defaultTheme').screens,
        '2xl': '1536px',
        '3xl': '1800px',
      },
    },

    extend: {
      fontFamily: {
        sans: ['Inter', 'Poppins', 'ui-sans-serif', 'system-ui'],
        heading: ['Poppins', 'Inter', 'ui-sans-serif'],
      },

      colors: {
        // brand palette
        gold: '#facc15',
        red:  '#b91c1c',
        black:'#18181b',
        white:'#ffffff',

        blue:  { DEFAULT:'#0a1f44', dark:'#061633' },
        // semantic
        primary:   '#facc15',
        secondary: '#0a1f44',
        neutral:   '#18181b',

        // accents
        'red-light' : '#f87171',
        'red-dark'  : '#7f1d1d',
        'gold-light': '#fde68a',
        'gold-dark' : '#bca004',
      },

      boxShadow: {
        'inner-gold' : 'inset 0 0 8px rgba(250,204,21,.6)',
        elevated     : '0 2px 10px rgba(0,0,0,.3)',
        ambient      : '0 25px 50px -12px rgba(0,0,0,.45)',
        'gold-aura'  : '0 0 12px rgba(250,204,21,.6)',
      },

      backdropBlur: { xs: '2px' },

      animation: {
        shine       : 'shine 2.5s linear infinite',
        'border-glint':'border-glint 2.5s ease-in-out infinite',
        'fade-in'   : 'fade-in .6s ease forwards',
        'slide-up'  : 'slide-up .6s cubic-bezier(.25,.8,.25,1) forwards',
        wiggle      : 'wiggle 1s ease-in-out infinite',
      },

      keyframes: {
        shine:       { '0%':{backgroundPosition:'200% 0'}, '100%':{backgroundPosition:'-200% 0'} },
        'border-glint':{
          '0%,100%':{borderColor:'#facc15'},
          '50%':{borderColor:'#fde68a'},
        },
        'fade-in':    { from:{opacity:0,transform:'translateY(4px)'}, to:{opacity:1,transform:'none'} },
        'slide-up':   { from:{transform:'translateY(20px)',opacity:0}, to:{transform:'none',opacity:1} },
        wiggle:       { '0%,100%':{transform:'rotate(-2deg)'}, '50%':{transform:'rotate(2deg)'} },
      },

      gradientColorStops: theme => ({
        'gold-glow': [theme('colors.gold'), theme('colors.gold-light')],
        'dark-glow': [theme('colors.black'), theme('colors.neutral')],
      }),
    },
  },

  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/container-queries'),
    // simple animate.css shortcuts (optional)
    require('tailwindcss-animate'),
  ],
};

