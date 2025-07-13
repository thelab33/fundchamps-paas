// postcss.config.js
module.exports = {
  plugins: [
    require('postcss-import'),
    require('@tailwindcss/postcss'),   // <-- use the new plugin
    require('autoprefixer'),
    require('postcss-nested')
  ]
}

