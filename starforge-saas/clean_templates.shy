#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# clean_templates.sh — Premium Jinja Template Sanitizer
# -----------------------------------------------------------------------------
# Author: Starforge DevOps Team
# License: MIT
# Description:
#   Safely decode URL-encoded Jinja2 tags across your HTML templates,
#   back up originals, and offer a --dry-run mode for CI/CD integration.
#
# Usage:
#   ./clean_templates.sh [--dry-run] [--backup-dir=<dir>] <templates_path>
#
# Options:
#   --dry-run           Show changes without applying them.
#   --backup-dir=DIR    Directory to store original templates
#                       (default: backups/YYYYMMDD_HHMMSS).
#
# Example:
#   ./clean_templates.sh --dry-run app/templates
#   ./clean_templates.sh --backup-dir=archive/backup app/templates/partials
# -----------------------------------------------------------------------------
set -euo pipefail

# Default settings
DRY_RUN=false
BACKUP_BASE=""

# Parse arguments
POSITIONAL=()
for ARG in "$@"; do
  case $ARG in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --backup-dir=*)
      BACKUP_BASE="${ARG#*=}"
      shift
      ;;
    *)
      POSITIONAL+=("$ARG")
      shift
      ;;
  esac
done
set -- "${POSITIONAL[@]}"

# Validate positional argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 [--dry-run] [--backup-dir=<dir>] <templates_path>"
  exit 1
fi
TEMPLATES_PATH="$1"

# Prepare backup directory if needed
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR=${BACKUP_BASE:-"backups/$TIMESTAMP"}

if [ "$DRY_RUN" = false ]; then
  mkdir -p "$BACKUP_DIR"
  echo "Backing up originals to $BACKUP_DIR..."
  find "$TEMPLATES_PATH" -type f -name '*.html' -exec cp --parents '{}' "$BACKUP_DIR" \;
else
  echo "[Dry-run] No backups or changes will be made."
fi

echo "Processing templates under $TEMPLATES_PATH..."

# Define sed expressions
SED_ARGS=(
  -e 's/{{%20url_for/{{ url_for/g'
  -e 's/)%20}}/) }}/g'
  -e 's/{{%20config\.GA_MEASUREMENT_ID%20}}/{{ config.GA_MEASUREMENT_ID }}/g'
  -e 's/%20//g'
)

# Iterate and patch
while IFS= read -r -d '' FILE; do
  if [ "$DRY_RUN" = true ]; then
    echo "--- Changes in $FILE ---"
    sed -n "${SED_ARGS[@]}" "$FILE" | sed 's/^/    /'
  else
    sed -i "${SED_ARGS[@]}" "$FILE"
    echo "Patched: $FILE"
  fi
done < <(find "$TEMPLATES_PATH" -type f -name '*.html' -print0)

echo "✅ Template sanitization complete!"
