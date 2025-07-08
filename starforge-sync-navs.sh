#!/usr/bin/env bash
set -e

TEMPLATE="app/templates/index.html"
BACKUP="app/templates/index.html.bak.$(date +%s)"
echo "🔒 Backing up $TEMPLATE → $BACKUP"
cp "$TEMPLATE" "$BACKUP"

# Get nav anchors and section IDs
grep -oP 'href="#\K[^"]+' "$TEMPLATE" | sort | uniq > /tmp/navs.txt
grep -oP '<section\s+[^>]*id=["'"'"']?\K[^"'"' >]+' "$TEMPLATE" | sort | uniq > /tmp/sections.txt

# Auto-create missing sections for navs
echo "✨ Checking for nav links missing <section>..."
comm -23 /tmp/navs.txt /tmp/sections.txt > /tmp/navs-missing-sections.txt

while read -r ID; do
  [ -z "$ID" ] && continue
  echo "  ➕ <section id=\"$ID\"> (auto-created for nav link #$ID)"
  echo "<section id=\"$ID\" class=\"py-12\"><!-- [Starforge] Auto-created for nav link: #$ID --></section>" >> "$TEMPLATE"
done < /tmp/navs-missing-sections.txt

# Report orphaned sections (not in nav)
echo "⚠️  Orphaned <section id> (not in nav):"
comm -13 /tmp/navs.txt /tmp/sections.txt | while read -r ID; do
  [ -n "$ID" ] && echo "  - <section id=\"$ID\">" || true
done

echo "📝 Starforge Nav/Section Sync complete! Backup at $BACKUP"

