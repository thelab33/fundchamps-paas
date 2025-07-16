#!/bin/bash

echo "🔧 Applying Starforge Patch..."

# 1. Fix SponsorForm import
echo "🔧 Fixing SponsorForm import..."
sed -i 's/from app.forms import SponsorForm/from app.forms.sponsor_form import SponsorForm/' app/routes/main.py

# 2. Add missing environment variables to .env file
echo "🔧 Ensuring environment variables are set..."
if ! grep -q "FLASK_DEBUG" .env; then
  echo "FLASK_DEBUG=True" >> .env
fi
if ! grep -q "DATABASE_URL" .env; then
  echo "DATABASE_URL=your_database_url" >> .env
fi
if ! grep -q "STRIPE_API_KEY" .env; then
  echo "STRIPE_API_KEY=your_stripe_api_key" >> .env
fi

# 3. Fix broken image and CSS paths
echo "🔧 Ensuring proper paths for static files..."
find app/templates -type f -exec sed -i "s|src=\"images/logo.webp\"|src=\"{{ url_for('static', filename='images/logo.webp') }}\"|" {} \;
find app/templates -type f -exec sed -i "s|href=\"css/tailwind.min.css\"|href=\"{{ url_for('static', filename='css/tailwind.min.css') }}\"|" {} \;
find app/templates -type f -exec sed -i "s|src=\"js/main.js\"|src=\"{{ url_for('static', filename='js/main.js') }}\"|" {} \;

# 4. Apply HTML validation fixes manually (based on the report)
echo "🔧 Applying HTML validation fixes..."
# Add additional fixes based on the report or use a tool like `htmlhint`

# 5. Set the FLASK_APP environment variable if needed and restart Flask to apply changes
echo "🔧 Restarting Flask app..."

export FLASK_APP=run.py  # Set the Flask entry point
flask run --reload

echo "✅ Patch complete!"
