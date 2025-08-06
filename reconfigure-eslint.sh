#!/bin/bash

# Check if .eslintignore exists and remove it
if [ -f ".eslintignore" ]; then
  echo "Removing deprecated .eslintignore file..."
  rm .eslintignore
else
  echo ".eslintignore file does not exist."
fi

# Update .eslintrc.js to remove the root key and apply new config
echo "Updating .eslintrc.js..."

cat > .eslintrc.js <<EOL
import { defineConfig } from 'eslint';

export default defineConfig({
  env: {
    browser: true,
    es2021: true,
    node: true, // For config files and Node-based scripts
  },
  parserOptions: {
    ecmaVersion: 12,
    sourceType: 'module', // allows import/export parsing
  },
  globals: {
    io: 'readonly', // socket.io global
    showDonationTicker: 'readonly',
    htmx: 'readonly',
    Alpine: 'readonly',
  },
  ignorePatterns: [
    'app/static/js/*.min.js', // Ignore minified scripts
    'node_modules/',         // Ignore node_modules directory
  ],
  extends: ['airbnb-base', 'prettier'],
  plugins: ['import'],
  rules: {
    'no-unused-vars': 'warn',
    'no-console': 'off',
    'no-undef': 'error',
    'no-prototype-builtins': 'off', // disable for legacy libs
  },
});
EOL

echo ".eslintrc.js has been updated!"

# Verify ESLint config
echo "Running ESLint with the new configuration..."

npx eslint --config .eslintrc.js .

echo "Reconfiguration complete! ESLint should now work without warnings."
