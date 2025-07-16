#!/bin/bash
echo "🌟 [Starforge Patch] Auto-fix Flask import/circular/seed issues..."

# 1. Ensure Faker is imported at top and fake = Faker() is after import
sed -i '/from faker import Faker/!b;n;s/^/fake = Faker()\n/' app/seeds.py

# 2. Remove any top-level 'from app import create_app' (should only be INSIDE the CLI function)
sed -i '/from app import create_app/d' app/seeds.py

# 3. Ensure no 'from .seeds import seed_demo' at the top of seeds.py
sed -i '/from .seeds import seed_demo/d' app/seeds.py

# 4. Patch app/__init__.py: move seed_demo import/registration inside create_app
awk '
/def create_app\(\):/ {print; print "    from .seeds import seed_demo\n    app.cli.add_command(seed_demo)"; found=1; next}
/from .seeds import seed_demo/ || /app.cli.add_command\(seed_demo\)/ {if (!found) next}
{print}
' app/__init__.py > app/__init__.py.tmp && mv app/__init__.py.tmp app/__init__.py

echo "✅ Patch complete! If you hit any other import errors, rerun me!"
echo "   Now run: flask run --reload --port 5001"
