#!/bin/bash
set -e

echo "🚀 Starting Starforge Flask-Login patch..."

# 1. Install flask-login
echo "📦 Installing Flask-Login..."
pip install flask-login

# 2. Patch app/extensions.py - add login_manager
EXT_FILE="app/extensions.py"
if ! grep -q "login_manager" "$EXT_FILE"; then
  echo "🔧 Adding login_manager to $EXT_FILE"
  echo -e "\nfrom flask_login import LoginManager\nlogin_manager = LoginManager()\n" >> "$EXT_FILE"
else
  echo "✅ login_manager already present in $EXT_FILE"
fi

# 3. Patch app/__init__.py - initialize login_manager and inject current_user
INIT_FILE="app/__init__.py"
if ! grep -q "login_manager.init_app(app)" "$INIT_FILE"; then
  echo "🔧 Updating $INIT_FILE to init Flask-Login and inject current_user"

  # Insert import for login_manager and current_user at top after existing imports
  sed -i "/from .extensions import db, migrate, socketio, cors/a from flask_login import current_user\nfrom .extensions import login_manager" "$INIT_FILE"

  # Insert login_manager.init_app(app) below other extension init lines
  sed -i "/socketio.init_app(app)/a \    login_manager.init_app(app)" "$INIT_FILE"

  # Insert user_loader function (stub)
  sed -i "/login_manager.init_app(app)/a \    \n    @login_manager.user_loader\n    def load_user(user_id):\n        from app.models import User  # Adapt to your user model\n        return User.query.get(int(user_id))\n" "$INIT_FILE"

  # Insert context processor for current_user injection just before return app
  sed -i "/register_blueprints(app)/i \    @app.context_processor\n    def inject_current_user():\n        return dict(current_user=current_user)\n" "$INIT_FILE"
else
  echo "✅ Flask-Login already configured in $INIT_FILE"
fi

# 4. Add note to your user model to import UserMixin (manual step reminder)
echo "⚠️ Reminder: Make sure your User model inherits from flask_login.UserMixin for compatibility."

echo "🎉 Flask-Login patch complete. Please adapt user_loader to your User model if needed."
