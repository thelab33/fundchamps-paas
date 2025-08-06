#!/bin/bash

# Update url_for references to use the correct blueprint prefix in templates
echo "Updating url_for references in templates..."

# Find all template files and replace 'url_for('donate')' with 'url_for('main.donate')'
find app/templates -type f -name "*.html" -exec sed -i 's|url_for("donate")|url_for("main.donate")|g' {} +

# Ensure the donate route is correctly linked to the 'main' blueprint in the code
echo "Updating the donate route in Python files..."

# Update Python routes to use the correct blueprint reference (main_bp)
sed -i 's|@app.route("/donate")|@main_bp.route("/donate")|g' app/routes/main_routes.py

# Check for the missing blueprint registration in the app initialization
echo "Ensuring blueprint registration in app initialization..."

# Make sure main_bp is registered in the app's __init__.py
if ! grep -q 'main_bp' app/__init__.py; then
    echo "Registering main_bp blueprint in app/__init__.py..."
    echo "from app.routes.main_routes import main_bp" >> app/__init__.py
    echo "app.register_blueprint(main_bp)" >> app/__init__.py
else
    echo "main_bp already registered in app/__init__.py."
fi

# Check for missing import in the main routes file
echo "Checking for missing imports..."

if ! grep -q 'from app.routes.main_routes import main_bp' app/routes/main_routes.py; then
    echo "Adding missing import for main_bp in main_routes.py..."
    sed -i '1i from app.routes.main_routes import main_bp' app/routes/main_routes.py
else
    echo "Import for main_bp already exists in main_routes.py."
fi

echo "Patch complete. Please restart your Flask app."
