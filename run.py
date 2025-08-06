#!/usr/bin/env python3
"""
    🚀 Starforge Flask SaaS Entrypoint (2025 Ultra Edition)
    -------------------------------------------------------
    Next-gen Flask app launcher with modern DX, CI/CD logs, and cloud/local flexibility.
"""

import os
import sys
import signal
import logging
from dotenv import load_dotenv

try:
    from flask_socketio import SocketIO
except ImportError:
    SocketIO = None

try:
    import eventlet
except ImportError:
    eventlet = None

# ──────────────────────────────────────────────
# 🛑 Graceful Shutdown Handler
# ──────────────────────────────────────────────
def handle_shutdown(signum, frame):
    logging.info(f"🛑 Received shutdown signal ({signum}). Exiting gracefully...")
    sys.exit(0)

# ──────────────────────────────────────────────
# ⚙️ Config Class Path Resolver
# ──────────────────────────────────────────────
def get_config_path():
    flask_config = os.getenv("FLASK_CONFIG")
    if flask_config:
        return flask_config

    env = os.getenv("FLASK_ENV", "production").lower()
    config_map = {
        "development": "app.config.DevelopmentConfig",
        "testing": "app.config.TestingConfig",
        "production": "app.config.ProductionConfig"
    }
    return config_map.get(env, "app.config.ProductionConfig")

# ──────────────────────────────────────────────
# 📣 Structured Logging Setup
# ──────────────────────────────────────────────
def setup_logging(debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

# ──────────────────────────────────────────────
# 🚀 Main Entrypoint
# ──────────────────────────────────────────────
def main():
    load_dotenv()

    config_path = get_config_path()
    debug_flag = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    reloader = debug_flag

    setup_logging(debug_flag)
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    # Import here so env vars are loaded
    from app import create_app

    logging.info("=" * 60)
    logging.info("🚀 Launching Starforge Flask SaaS App")
    logging.info(f"🌎 ENV        = {os.getenv('FLASK_ENV', 'production')}")
    logging.info(f"⚙️ CONFIG     = {config_path}")
    logging.info(f"🐞 Debug      = {debug_flag}")
    logging.info(f"🔌 Host:Port  = {host}:{port}")
    logging.info("=" * 60)
    # Pro: Print a clickable URL for local/dev
    if host in ("127.0.0.1", "0.0.0.0", "localhost"):
        url = f"http://127.0.0.1:{port}"
        logging.info(f"💻 Local Dev URL: \033[1;34m{url}\033[0m")
    sys.stdout.flush()

    try:
        app = create_app(config_path)

        # --- SocketIO/WS support ---
        if SocketIO:
            async_mode = 'eventlet' if eventlet else 'threading'
            socketio = SocketIO(app, async_mode=async_mode)
            socketio.run(
                app,
                host=host,
                port=port,
                debug=debug_flag,
                use_reloader=reloader,
                allow_unsafe_werkzeug=True,  # Needed for newer Flask/SocketIO
            )
        else:
            # Pure Flask fallback
            app.run(
                host=host,
                port=port,
                debug=debug_flag,
                use_reloader=reloader,
            )
    except Exception as e:
        logging.error(f"❌ Failed to start Starforge Flask app: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

