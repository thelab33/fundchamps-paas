#!/bin/bash
set -e

echo "🛠️ Patching config imports to use app.config..."

# 1. Fix manage.py config import usage
if grep -q 'create_app("config.DevelopmentConfig")' manage.py; then
  sed -i 's/create_app("config.DevelopmentConfig")/create_app("app.config.DevelopmentConfig")/g' manage.py
  echo "✅ Patched manage.py create_app config string"
fi

# 2. Fix starforge_audit.py config import usage
if grep -q 'create_app("config.DevelopmentConfig")' starforge_audit.py; then
  sed -i 's/create_app("config.DevelopmentConfig")/create_app("app.config.DevelopmentConfig")/g' starforge_audit.py
  echo "✅ Patched starforge_audit.py create_app config string"
fi

# 3. Patch create_app() in app/__init__.py to accept class or string for config
INIT_FILE="app/__init__.py"

if ! grep -q 'def create_app(config_class: Union[str, Type] = None) -> Flask:' "$INIT_FILE"; then
  echo "✅ Patching create_app() signature and logic in app/__init__.py"

  # Insert imports at top if missing
  if ! grep -q 'from typing import Union, Type' "$INIT_FILE"; then
    sed -i '1ifrom typing import Union, Type' "$INIT_FILE"
  fi

  # Update create_app signature and config loading logic
  # Backup first
  cp "$INIT_FILE" "${INIT_FILE}.bak"

  # Use perl to replace the entire create_app definition and start of body
  perl -0777 -i -pe '
    s/def create_app\(config_class: .*? = None\) -> Flask:/def create_app(config_class: Union[str, Type] = None) -> Flask:/s;
    s/app = Flask\(.*?\n\n\s*# Load configuration\n\s*if isinstance\(config_class, str\):\n\s*app.config.from_object\(config_class\)\n\s*elif config_class is not None:\n\s*app.config.from_object\(config_class\)\n\s*else:\n\s*app.config.from_object\(os.getenv\("FLASK_CONFIG", "app.config.DevelopmentConfig"\)\)\n\n/app = Flask(__name__, static_folder="static", template_folder="templates")\n\n    # Load configuration\n    if config_class is None:\n        from app.config import DevelopmentConfig\n        config_class = DevelopmentConfig\n\n    if isinstance(config_class, str):\n        app.config.from_object(config_class)\n    else:\n        app.config.from_object(config_class)\n\n/gs;
  ' "$INIT_FILE"

else
  echo "ℹ️ create_app() signature already patched in app/__init__.py"
fi

echo "🎉 Patch complete! Remember to restart your Flask server."
