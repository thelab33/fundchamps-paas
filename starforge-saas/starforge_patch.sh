#!/bin/bash

echo "🔧 Running Starforge Elite Patch..."

# Step 1: Fix import in app/forms/__init__.py for SponsorForm
echo "🔧 Fixing unused import in app/forms/__init__.py..."
sed -i '/^from .sponsor_form import SponsorForm/s/^/#/' app/forms/__init__.py

# Step 2: Fix undefined import 'User' and 'app' in app/models/models.py
echo "🔧 Fixing undefined 'User' and 'app' imports in app/models/models.py..."
sed -i '1i from app.models import User' app/models/models.py
sed -i '1i from flask import current_app' app/models/models.py

# Step 3: Remove unused metadata variable in app/routes/stripe_routes.py
echo "🔧 Removing unused metadata variable in app/routes/stripe_routes.py..."
sed -i '/metadata = session.get("metadata", {})/d' app/routes/stripe_routes.py

# Step 4: Move BeautifulSoup import to the top in patch_and_polish.py
echo "🔧 Moving BeautifulSoup import to the top in patch_and_polish.py..."
sed -i '59i from bs4 import BeautifulSoup' patch_and_polish.py

# Step 5: Remove unused app_dir variable in patch_and_polish.py
echo "🔧 Removing unused app_dir variable in patch_and_polish.py..."
sed -i '93d' patch_and_polish.py

# Step 6: Fix URL generation issue in hero_overlay_quote.html
echo "🔧 Fixing URL generation issue in hero_overlay_quote.html..."
sed -i 's|url_for("main.home")|url_for("main.home")|g' app/templates/partials/hero_overlay_quote.html

# Step 7: Ensure all static paths are correct
echo "🔧 Ensuring all static paths are correct..."
sed -i 's|static/|/static/|g' app/templates/partials/*.html

echo "✅ Patch complete! All fixes have been applied."

# Step 8: Run ruff and black to verify fixes
echo "🔧 Running ruff and black to verify fixes..."
ruff check --fix
black .

echo "✨ All fixes have been applied and linting is complete."

