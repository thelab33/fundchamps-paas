#!/usr/bin/env bash
# Starforge one‑shot patch script – brings your repo in line with the
# fixes we discussed: cleans up app/__init__.py, injects an index route,
# and bumps socket.io CORS settings. Run from project root:
#   chmod +x scripts/starforge_patch.sh && ./scripts/starforge_patch.sh
set -euo pipefail

bold() { printf "\e[1m%s\e[0m\n" "$1"; }
info() { printf "[\e[34mINFO\e[0m] %s\n" "$1"; }
warn() { printf "[\e[33mWARN\e[0m] %s\n" "$1"; }

PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
cd "$PROJECT_ROOT"

########################################
# 1. Patch app/__init__.py              #
########################################
INIT_FILE="app/__init__.py"
if [[ ! -f $INIT_FILE ]]; then
  warn "Expected $INIT_FILE but it was not found – skipping init patch."
else
  info "➜ Cleaning stray demo block from $INIT_FILE"
  # Remove everything from the accidental inline 'app/routes.py' snippet onward
  sed -i.bak '/^# app\/routes.py/,$d' "$INIT_FILE"

  # Ensure create_app is re‑exported
  if ! grep -q '__all__' "$INIT_FILE"; then
    echo -e "\n__all__ = ['create_app']" >> "$INIT_FILE"
    info "   Added __all__ export."
  fi

  # Ensure socketio.init_app has cors_allowed_origins
  if grep -q "socketio.init_app(app)" "$INIT_FILE"; then
    sed -i "s/socketio.init_app(app)/socketio.init_app(app, cors_allowed_origins=cors_origins)/" "$INIT_FILE"
    info "   socketio.init_app cors_allowed_origins added."
  fi
fi

########################################
# 2. Ensure app/routes.py exists        #
########################################
ROUTES_FILE="app/routes.py"
if [[ -f $ROUTES_FILE ]]; then
  info "➜ app/routes.py already exists – leaving intact."
else
  info "➜ Creating minimal app/routes.py with main_bp and index route."
  mkdir -p app
  cat > "$ROUTES_FILE" <<'PY'
from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Landing page – customize or swap with SPA send_file."""
    try:
        return render_template("index.html")
    except Exception:  # pragma: no cover – fallback when template missing
        return {"message": "Starforge API 🛠"}
PY
fi

########################################
# 3. Reminder for config update         #
########################################
bold "✔ Patch completed. Next steps:"
cat <<'EOS'
1. Verify   : flask routes | head
2. Run      : flask run --reload
3. Enjoy 🤘 : http://127.0.0.1:5000/
EOS
