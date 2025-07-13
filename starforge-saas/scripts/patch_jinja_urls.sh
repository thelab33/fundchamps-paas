#!/usr/bin/env bash
#
# scripts/patch_jinja_urls.sh
# Starforge patch: fix URL-encoded Jinja tags in all templates

set -euo pipefail

# 1) Fix any {{%20url_for(...)%20}} → {{ url_for(...) }}
# 2) Fix any {{%20config.GA_MEASUREMENT_ID%20}} → {{ config.GA_MEASUREMENT_ID }}
# 3) Trim stray “%20”s elsewhere
find app/templates -type f -name '*.html' -print0 \
  | xargs -0 sed -i \
    -e "s/{{%20url_for/{{ url_for/g" \
    -e "s/)%20}}/) }}/g" \
    -e "s/{{%20config\.GA_MEASUREMENT_ID%20}}/{{ config.GA_MEASUREMENT_ID }}/g" \
    -e "s/%20//g"

echo "✅ All Jinja URL‐encoding artifacts cleaned up!"
