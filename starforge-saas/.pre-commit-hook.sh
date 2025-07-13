#!/bin/bash
echo "🔍 Running pre-commit .env check..."
if command -v dotenv-linter &> /dev/null; then
  dotenv-linter .env
else
  echo "⚠️ dotenv-linter not found. Run: pip install dotenv-linter"
fi

echo "🔍 Scanning for secrets..."
if command -v detect-secrets &> /dev/null; then
  detect-secrets scan > .secrets.baseline
else
  echo "⚠️ detect-secrets not found. Run: pip install detect-secrets"
fi
