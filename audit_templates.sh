#!/bin/bash
set -e

context_file="context.json"
templates=("templates/index.html" "templates/base.html")

echo "Running Jinja lint checks..."
jinja-lint "${templates[@]}"

echo "Rendering templates with strict context to catch undefined variables..."
for tpl in "${templates[@]}"; do
  echo "Checking $tpl..."
  jinja2 "$tpl" --format=json --strict --context="$context_file" > /dev/null
done

echo "All templates passed lint and render checks ✅"
