# manage.py — Flask CLI & entrypoint for Connect ATX Elite PaaS
#!/usr/bin/env python
"""
Traditional Flask entry-point without SocketIO, powering Flask CLI commands:
  $ flask shell
  $ flask db migrate
  $ flask run
Also allows:
  $ python manage.py             # local test run
"""

from __future__ import annotations
import os
from app import create_app
from app.extensions import db, migrate

# ─── Resolve Config via FLASK_CONFIG or Default to Development ──────
cfg_path = os.getenv("FLASK_CONFIG", "config.DevelopmentConfig")
app = create_app(cfg_path)

# ─── Initialize Migrations for Flask CLI ──────────────────────────
migrate.init_app(app, db)

# ─── CLI: flask commands live here (shell, db, run) ───────────────
# (Flask-CLI auto-discovers `app`)

if __name__ == "__main__":
    # Local dev server with debug toggle
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=app.debug,
    )
