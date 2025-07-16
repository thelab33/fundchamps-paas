#!/bin/bash
set -e

TEMPLATES_DIR="app/templates"
REPORT="reports/img_tag_audit.txt"

mkdir -p reports
echo "Image Tag Audit Report - $(date)" > "$REPORT"
echo "Scanning templates for malformed <img> tags..." >> "$REPORT"
echo "-----------------------------------------------" >> "$REPORT"

# Look for <img tags that do NOT have properly formed src attributes or look suspicious
grep -r --include \*.html --include \*.jinja2 -n '<img' "$TEMPLATES_DIR" | while read -r line; do
  file=$(echo "$line" | cut -d: -f1)
  lineno=$(echo "$line" | cut -d: -f2)
  content=$(echo "$line" | cut -d: -f3-)

  # Check if src attribute is missing or malformed
  if ! echo "$content" | grep -q 'src=['\"'\'']'; then
    echo "[$file:$lineno] Missing or malformed src attribute in <img> tag:" >> "$REPORT"
    echo "  $content" >> "$REPORT"
    echo >> "$REPORT"
  fi

  # Check if src value looks like a template variable (should be OK) but also catch unescaped/unfinished tags
  if echo "$content" | grep -q 'src="{{' && ! echo "$content" | grep -q '}}"'; then
    echo "[$file:$lineno] Possibly unclosed src template expression:" >> "$REPORT"
    echo "  $content" >> "$REPORT"
    echo >> "$REPORT"
  fi
done

echo "Scan complete. See $REPORT for details."
