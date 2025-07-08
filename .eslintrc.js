module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true, // For config files and Node-based scripts
  },
  parserOptions: {
    ecmaVersion: 12,
    sourceType: "module", // allows import/export parsing
  },
  globals: {
    io: "readonly", // socket.io global
    showDonationTicker: "readonly",
    htmx: "readonly",
    Alpine: "readonly",
  },
  ignorePatterns: [
    "app/static/js/*.min.js", // ignore vendor/minified scripts
    "node_modules/",
  ],
  extends: ["airbnb-base", "prettier"],
  plugins: ["import"],
  rules: {
    "no-unused-vars": "warn",
    "no-console": "off",
    "no-undef": "error",
    "no-prototype-builtins": "off", // disable for legacy libs
  },
};

