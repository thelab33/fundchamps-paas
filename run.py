"""
run.py – Starforge Flask entry-point
-----------------------------------
Launch with:
    python run.py          # production config by default
    FLASK_CONFIG=config.DevelopmentConfig FLASK_DEBUG=1 python run.py
"""

import os
from app import create_app, socketio

# ------------------------------------------------------------------
# Config selection
# ------------------------------------------------------------------
config_path = os.getenv("FLASK_CONFIG") or "config.ProductionConfig"
app = create_app(config_path)

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
if __name__ == "__main__":
    # Enable debug only when FLASK_DEBUG=1 (or true-ish)
    debug_flag = os.getenv("FLASK_DEBUG", "0") in ("1", "true", "True")

    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=debug_flag,
        use_reloader=debug_flag,   # auto-reload only in dev
    )

