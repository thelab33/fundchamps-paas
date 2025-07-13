#!/bin/bash
mkdir -p reports

echo "🔍 Auditing Tailwind class/id usage..."
grep -roPhn '(class|id)="[^"]+"' app/templates | sort | uniq -c | sort -nr > reports/class_usage.txt

echo "🖼️ Auditing <img> tag usage..."
grep -rPo '<img[^>]+>' app/templates | sort > reports/img_tags.txt

echo "📂 Jinja static refs..."
grep -roPh 'url_for\([^)]+\)' app/templates | sort | uniq -c | sort -nr > reports/static_refs.txt

echo "🔁 Flagging repeated text blocks..."
grep -rPo "(Connect ATX Elite|Coach Angel Rodriguez|StripeStripe|PayPalPayPal)" app/templates | sort | uniq -c > reports/dupe_phrases.txt

echo "🧱 Checking raw src= paths..."
grep -rPo 'src="[^"]+"' app/templates | cut -d'"' -f2 | sort | uniq > reports/image_paths_raw.txt

echo "🚨 Detecting missing images..."
cat reports/image_paths_raw.txt | grep 'static/' | while read -r path; do test -f "$path" || echo "MISSING: $path"; done > reports/missing_images.txt

echo "⚠️ Inline JS audit (onclick)..."
grep -rPo '<[a-z]+\s[^>]*>' app/templates | grep -i 'onclick' | sort > reports/dom_inline_js.txt

echo "🧼 Buttons missing type..."
grep -rPo '<button[^>]*>' app/templates | grep -v 'type=' | sort > reports/button_without_type.txt

echo "🧭 Heading structure..."
grep -rPo '<(h1|h2|h3)[^>]*>' app/templates | sort > reports/heading_hierarchy.txt

echo "🏎️ Image perf attributes..."
grep -rPo 'fetchpriority|loading="[^"]+|decoding="[^"]+' app/templates | sort | uniq -c > reports/img_perf_attrs.txt

echo "✅ Audit complete — check ./reports/"
