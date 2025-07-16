#!/bin/bash
set -e

echo "🔧 Fixing misused Jinja control syntax in templates..."

# Define templates directory
TEMPLATES_DIR="app/templates"

# Backup all HTML templates first
echo "Backing up all HTML templates..."
find "$TEMPLATES_DIR" -type f -name '*.html' -exec cp {} {}.bak.$(date +%s) \;

# Fix common misuses: {{if ...}}, {{for ...}}, {{else}}, {{endif}} inside HTML templates
echo "Patching files..."

# Replace {{if ...}} with {% if ... %}
find "$TEMPLATES_DIR" -type f -name '*.html' -exec sed -i -E 's/\{\{\s*if\s+/\\{% if /g' {} \;

# Replace {{for ...}} with {% for ... %}
find "$TEMPLATES_DIR" -type f -name '*.html' -exec sed -i -E 's/\{\{\s*for\s+/\\{% for /g' {} \;

# Replace {{else}} with {% else %}
find "$TEMPLATES_DIR" -type f -name '*.html' -exec sed -i -E 's/\{\{\s*else\s*\}\}/\\{% else %}/g' {} \;

# Replace {{endif}} or {{end if}} or {{endfor}} with correct endings
find "$TEMPLATES_DIR" -type f -name '*.html' -exec sed -i -E 's/\{\{\s*end(if| for|for| end if)\s*\}\}/\\{% end\1 %}/g' {} \;

echo "✅ Jinja control syntax fix complete! Review backups (*.bak.*) before committing."
