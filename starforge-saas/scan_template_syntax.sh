#!/bin/bash
# scan_template_syntax.sh - Scan templates for suspicious unescaped quotes or unclosed tags

TEMPLATE_DIR="app/templates"
REPORT="reports/template_syntax_issues.txt"

mkdir -p reports
echo "Template Syntax Scan Report - $(date)" > "$REPORT"
echo "Scanning $TEMPLATE_DIR for unescaped quotes, unclosed tags, and suspicious Jinja syntax..." >> "$REPORT"
echo "------------------------------------------------------" >> "$REPORT"

# Pattern explanations:
# 1) Unescaped quotes in attribute values (look for " or ' followed by a quote without escape)
# 2) Unclosed Jinja blocks: lines with {% if without matching endif, {% for without endfor, etc.
# 3) Unmatched braces: lines with { but no }, or < without >

grep -r --include=\*.{html,jinja2} -nE '=[^"'"'"']*["'"'"'][^"'"'"']*["'"'"']|{%[^%]*$|{{[^}]*$|{[^}]*$' "$TEMPLATE_DIR" | while IFS=: read -r file line content; do
  echo "Potential syntax issue in $file at line $line:" >> "$REPORT"
  echo "  $content" >> "$REPORT"
  echo "------------------------------------------------------" >> "$REPORT"
done

echo "Scan complete. See $REPORT for details."
