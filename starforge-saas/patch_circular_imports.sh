#!/bin/bash

set -e

echo "🌟 [Starforge Patch] Flask circular import auto-fixer..."

# 1. PATCH app/__init__.py
if grep -q 'from .seeds import seed_demo' app/__init__.py; then
    echo "🔹 Patching app/__init__.py..."
    # Remove all top-level seed_demo imports
    sed -i '/from .seeds import seed_demo/d' app/__init__.py

    # Add CLI import inside create_app() (if not already present)
    awk '
        BEGIN {done=0}
        /^def create_app/ {print; print "    from .seeds import seed_demo\n    app.cli.add_command(seed_demo)"; done=1; next}
        {print}
        END {if (!done) print "# [PATCH NOTE] def create_app() not found!"; }
    ' app/__init__.py > app/__init__.py.patched && mv app/__init__.py.patched app/__init__.py
    echo "✅ Patched app/__init__.py"
fi

# 2. PATCH app/seeds.py (remove self-imports)
echo "🔹 Cleaning up app/seeds.py imports..."
sed -i '/from .seeds import seed_demo/d' app/seeds.py
sed -i '/from app.seeds import seed_demo/d' app/seeds.py

# 3. (Optional) Remove circular import artifacts from old model hacks
echo "🔹 Cleaning up FooBar imports (if any)..."
sed -i '/from .foo_bar/d' app/models/__init__.py 2>/dev/null || true
sed -i 's/"FooBar",//g' app/models/__init__.py 2>/dev/null || true

echo "🌟 All done! You are now circular-import-free. 🚀"
echo "Run: flask run --reload --port 5001"

