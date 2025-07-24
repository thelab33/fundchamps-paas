// eslint.config.js
export default {
  root: true,
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:import/errors",
    "plugin:import/warnings",
    "plugin:import/typescript",
  ],
  parserOptions: {
    ecmaVersion: 12,
    sourceType: "module",
  },
  rules: {
    // Customize your linting rules here
  },
  ignorePatterns: ["node_modules/", "dist/", "app/__pycache__/"],
};
