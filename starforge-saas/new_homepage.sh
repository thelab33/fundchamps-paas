#!/usr/bin/env bash
# new_homepage.sh — Lightning SaaS Org Homepage Generator

set -e

ORG="${1:-}"
BLOCKS="${2:-}"

usage() {
  echo "Usage: $0 --org \"Org Name\" --blocks partial1,partial2,partial3,... [--output filename]"
  exit 1
}

# Parse CLI args (support --org, --blocks, --output)
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --org) ORG="$2"; shift ;;
    --blocks) BLOCKS="$2"; shift ;;
    --output) OUTPUT="$2"; shift ;;
    *) usage ;;
  esac
  shift
done

[ -z "$ORG" ] && echo "❌ Please provide an --org name." && usage
[ -z "$BLOCKS" ] && echo "❌ Please provide a --blocks list." && usage

OUTPUT="${OUTPUT:-app/templates/index.html}"
PARTIALS_PATH="app/templates/partials"

cat > "$OUTPUT" <<EOF
{# ================== $OUTPUT (Generated SaaS Homepage) ================== #}
{% extends "base.html" %}
{% block title %}Home · {{ team.team_name if team else '$ORG' }}{% endblock %}

{% block content %}
EOF

IFS=',' read -ra PARTIALS <<< "$BLOCKS"
for PARTIAL in "${PARTIALS[@]}"; do
  echo "  {% include \"partials/${PARTIAL}.html\" %}" >> "$OUTPUT"
done

cat >> "$OUTPUT" <<EOF
{% endblock %}
EOF

echo "✅ $OUTPUT generated for '$ORG' with blocks: $BLOCKS"
