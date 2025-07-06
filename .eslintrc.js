module.exports = {
  env: { browser: true, es2021: true },
  extends: ["airbnb-base", "prettier"],
  plugins: ["import"],
  rules: {
    "no-unused-vars": "warn",
    "no-console": "off",
    "no-undef": "error"
  }
};
