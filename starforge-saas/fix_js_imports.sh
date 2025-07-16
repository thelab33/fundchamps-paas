#!/bin/bash
set -e

BASE_JS_DIR="app/static/js"

echo "Fixing JS import paths..."

find "$BASE_JS_DIR" -type f -name "*.js" | while read -r jsfile; do
  echo "Processing $jsfile"

  # Fix import statements from '../js/' or './js/' to './'
  sed -i -E \
    -e "s|(import .+ from ['\"])\.\./js/|\1./|g" \
    -e "s|(import .+ from ['\"])\./js/|\1./|g" \
    -e "s|(require\(['\"])\.\./js/|\1./|g" \
    -e "s|(require\(['\"])\./js/|\1./|g" \
    "$jsfile"
done

echo "✅ JS import paths fixed!"
