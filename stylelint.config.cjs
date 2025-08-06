/** @type {import('stylelint').Config} */
module.exports = {
  extends: [
    'stylelint-config-standard',
    'stylelint-config-tailwindcss',
  ],
  plugins: ['stylelint-order'],
  ignoreFiles: [
    '**/*.min.css',
    '**/*.map',
    'dist/**',
    'build/**',
    'app/static/css/tailwind.min.css',
    'app/static/css/**/*.min.css',
    'app/static/css/vendor/**',
    'app/static/css/output.css',
  ],
  rules: {
    'at-rule-no-unknown': [
      true, 
      { ignoreAtRules: ['tailwind', 'apply', 'responsive', 'screen', 'variants', 'layer'] },
    ],
    'selector-class-pattern': null,

    // 🔕 Turn off the noisy rule
    'declaration-block-single-line-max-declarations': null,

    // Keep this permissive
    'unit-allowed-list': [
      [
        'px', 'rem', 'em', '%', 'vh', 'vw', 'vmin', 'vmax', 'ch', 'ex',
        'deg', 'rad', 'turn', 's', 'ms', 'cm', 'mm', 'in', 'pt', 'pc', 'fr',
      ],
      { severity: 'warning' },
    ],

    'order/properties-alphabetical-order': true,
  },
  reportNeedlessDisables: true,
};

