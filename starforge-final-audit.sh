#!/bin/bash
# ==== STARFORGE FINAL STACK + HTML/JINJA AUDIT ====
set -euo pipefail

RED='\033[0;31m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'; BLUE='\033[0;36m'; NC='\033[0m'
echo -e "${YELLOW}🚀 [Starforge] Launch-Readiness Audit: $(date)${NC}"
AUDIT_TIME=$(date +%s)
TEMPL_DIR="app/templates"
STATIC_DIR="app/static"
CSS_FILE="$STATIC_DIR/css/globals.css"
BACKUP="$CSS_FILE.bak.$AUDIT_TIME"
REPORT="starforge-audit-report.$AUDIT_TIME.log"

# --- Safety Backups ---
echo -e "${BLUE}🔒 Backing up globals.css → $BACKUP${NC}"
cp "$CSS_FILE" "$BACKUP"

# --- Section Inventory ---
echo -e "\n${GREEN}🔍 Auditing <section> structure and IDs...${NC}" | tee $REPORT
grep -oP '<section\s+[^>]*id=["'\'']?\K[^"\' >]+' $TEMPL_DIR/index.html | nl -w2 -s'. ' | tee -a $REPORT
SEC_COUNT=$(grep -oP '<section\s+[^>]*id=["'\'']?\K[^"\' >]+' $TEMPL_DIR/index.html | wc -l)

# --- Dead/Nav Link Check ---
echo -e "\n${BLUE}🧭 Checking nav <a href=#...> anchors:${NC}" | tee -a $REPORT
grep -oP 'href="#\K[^"]+' $TEMPL_DIR/index.html | sort | uniq | tee -a $REPORT
NAV_COUNT=$(grep -oP 'href="#\K[^"]+' $TEMPL_DIR/index.html | sort | uniq | wc -l)

# --- Unused Section ID Detector ---
echo -e "\n${GREEN}🧹 Checking for unused section IDs (defined but not linked in nav):${NC}" | tee -a $REPORT
grep -oP '<section\s+[^>]*id=["'\'']?\K[^"\' >]+' $TEMPL_DIR/index.html | while read id; do
  if ! grep -q "href=\"#${id}\"" $TEMPL_DIR/index.html; then
    echo -e "${RED}❗ Unlinked section: $id${NC}" | tee -a $REPORT
  fi
done

# --- Missing Include/Partial Audit ---
echo -e "\n${BLUE}🧩 Scanning for unused or missing includes/partials...${NC}" | tee -a $REPORT
PARTIALS_COUNT=0
find $TEMPL_DIR/partials -name "*.html" | while read f; do
  BASE=$(basename "$f")
  PARTIALS_COUNT=$((PARTIALS_COUNT + 1))
  if ! grep -q "$BASE" $TEMPL_DIR/index.html; then
    echo -e "${YELLOW}⚠️ Partial not included in index.html: $BASE${NC}" | tee -a $REPORT
  fi
done

# --- Button and CTA Inventory ---
echo -e "\n${GREEN}🚨 Button/CTA/Modal Audit:${NC}" | tee -a $REPORT
grep -oP '(button|a)[^>]*>(.*?)</(button|a)>' $TEMPL_DIR/index.html | grep -iE 'sponsor|donate|join|champion|modal' | tee -a $REPORT

# --- Static Asset 404/Existence Check ---
echo -e "\n${BLUE}📦 Static Asset Check (images/fonts/icons):${NC}" | tee -a $REPORT
ASSET_COUNT=0
grep -oP 'static[\/\w\-\.\d]+' $TEMPL_DIR/index.html | sort | uniq | while read asset; do
  ASSET_COUNT=$((ASSET_COUNT + 1))
  if [ ! -f "$STATIC_DIR/${asset#static/}" ]; then
    echo -e "${RED}❌ Missing static asset: $STATIC_DIR/${asset#static/}${NC}" | tee -a $REPORT
  else
    echo -e "${GREEN}✅ $asset found${NC}"
  fi
done

# --- CSS Variable Usage Audit ---
echo -e "\n${YELLOW}🎨 Custom CSS Variables Used:${NC}" | tee -a $REPORT
CSSVAR_COUNT=$(grep -oP 'var\(--[a-zA-Z0-9\-]+\)' $CSS_FILE | sort | uniq | tee -a $REPORT | wc -l)

# --- Bonus: Jinja Error Linting ---
echo -e "\n${BLUE}🔎 Jinja Variable Usage Check:${NC}" | tee -a $REPORT
grep -oP '\{\{\s*[a-zA-Z0-9_\.]+\s*\}\}' $TEMPL_DIR/index.html | sort | uniq | tee -a $REPORT

# --- Summary Recap ---
echo -e "\n${YELLOW}🚦 [Starforge] Audit Summary:${NC}"
echo -e " - Sections: $SEC_COUNT"
echo -e " - Nav Links: $NAV_COUNT"
echo -e " - Custom CSS vars: $CSSVAR_COUNT"

echo -e "\n${BLUE}✅ [Starforge] Audit complete! See: $REPORT${NC}"
echo -e "${GREEN}🔥 Review warnings above. Ready for production flex!\n${NC}"

