#!/bin/bash
echo "📊 Starforge App Checkup: Routes + Blueprints + Assets"

mkdir -p reports

echo "📍 Dumping all Flask routes..."
flask routes > reports/routes_list.txt && tail -n 10 reports/routes_list.txt

echo "📁 Blueprint Tree Audit..."
tree app/routes > reports/blueprints_tree.txt && cat reports/blueprints_tree.txt

echo "🧠 Blueprint Definitions..."
grep -R "Blueprint(" app/routes > reports/blueprint_defs.txt && cat reports/blueprint_defs.txt

echo "🔗 Static Asset Path Usage in Templates..."
grep -R "url_for('static" app/templates > reports/static_path_usage.txt && tail -n 10 reports/static_path_usage.txt

echo "📂 Model List..."
ls app/models/*.py > reports/models_list.txt && cat reports/models_list.txt

echo "✅ Checkup complete. Review the reports/*.txt files for full audit."
