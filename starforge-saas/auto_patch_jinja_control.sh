#!/bin/bash
set -e

echo "🔍 Starting Jinja control syntax auto-patch..."

# Backup all template files before patching
find app/templates -type f -name '*.html' -exec bash -c '
  for file; do
    cp "$file" "${file}.bak.$(date +%s)"
    echo "Backup saved: $file.bak"
  done
' bash {} +

# Replace common mistaken control statement syntax in all .html templates
find app/templates -type f -name '*.html' -exec sed -i -E '
  s/\{\{\s*(set|if|for|endif|endfor|else|elif|block|endblock|include|extends|macro|endmacro)\s+/ {%\1 /g;
  s/\s*(endif|endfor|endblock|endmacro)\s*\}\}/ %}/g;
  s/\{\{\s*else\s*\}\}/ {% else %}/g;
  s/\{\{\s*elif\s+([^}]+)\s*\}\}/ {% elif \1 %}/g;
  s/\{\{\s*include\s+["'"'"'][^"'"'"']+["'"'"']\s*\}\}/ {% include \0 %}/g
' {} +

echo "✅ Jinja control syntax auto-patch complete! Please review backups (*.bak.*)."
