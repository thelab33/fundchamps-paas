#!/usr/bin/env python3
import os
import sys
import signal
import logging
from dotenv import load_dotenv
from flask import render_template  # ✅ Needed for homepage route

# ─────────────────────────────────────────────────────────────
# 🛑 Graceful Shutdown Handler
# ─────────────────────────────────────────────────────────────
def handle_shutdown(signum, frame):
    logging.info(f"🛑 Received shutdown signal ({signum}). Exiting gracefully...")
    sys.exit(0)

# ─────────────────────────────────────────────────────────────
# ⚙️ Resolve Config Class Path (e.g., app.config.DevelopmentConfig)
# ─────────────────────────────────────────────────────────────
def get_config_path():
    flask_config = os.getenv("FLASK_CONFIG")
    if flask_config:
        return flask_config

    env = os.getenv("FLASK_ENV", "production").lower()
    return {
        "development": "app.config.DevelopmentConfig",
        "testing": "app.config.TestingConfig",
        "production": "app.config.ProductionConfig"
    }.get(env, "app.config.ProductionConfig")

# ─────────────────────────────────────────────────────────────
# 📣 Setup Logging Output Format + Level
# ─────────────────────────────────────────────────────────────
def setup_logging(debug: bool):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

# ─────────────────────────────────────────────────────────────
# 🚀 Entry Point
# ─────────────────────────────────────────────────────────────
def main():
    load_dotenv()

    # Parse configuration
    config_path = get_config_path()
    debug_flag = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")

    # Setup log format
    setup_logging(debug_flag)

    logging.info("=" * 60)
    logging.info("🚀 Launching Starforge Flask app")
    logging.info(f"🌎 ENV        = {os.getenv('FLASK_ENV', 'production')}")
    logging.info(f"⚙️ CONFIG     = {config_path}")
    logging.info(f"🐞 Debug      = {debug_flag}")
    logging.info(f"🔌 Host:Port  = {host}:{port}")
    logging.info("=" * 60)

    # Graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        from app import create_app, socketio
        app = create_app(config_path)

        # ✅ Add homepage route
        @app.route("/")
        def homepage():
            return render_template("index.html")

        # Run with Flask-SocketIO
        socketio.run(
            app,
            host=host,
            port=port,
            debug=debug_flag,
            use_reloader=debug_flag,
            allow_unsafe_werkzeug=True,
        )

    except Exception as e:
        logging.error(f"❌ Failed to start Starforge Flask app: {e}", exc_info=True)
        sys.exit(1)

    return app

if __name__ == "__main__":
    main()

