#!/usr/bin/env python3
"""
    🚀 Starforge Flask SaaS Entrypoint
    ----------------------------------
    Handles app creation, config, graceful shutdown, and real-time server launch.
    Elite-polished for production and local development.
"""
import os
import sys
import signal
import logging
from dotenv import load_dotenv
from flask import render_template

# ──────────────────────────────────────────────
# 🛑 Graceful Shutdown Handler
# ──────────────────────────────────────────────
def handle_shutdown(signum, frame):
    logging.info(f"🛑 Received shutdown signal ({signum}). Exiting gracefully...")
    sys.exit(0)

# ──────────────────────────────────────────────
# ⚙️ Config Class Path Resolver (auto-maps env)
# ──────────────────────────────────────────────
def get_config_path() -> str:
    # Allow override for advanced ops (FLASK_CONFIG)
    flask_config = os.getenv("FLASK_CONFIG")
    if flask_config:
        return flask_config
    env = os.getenv("FLASK_ENV", "production").lower()
    return {
        "development": "app.config.DevelopmentConfig",
        "testing": "app.config.TestingConfig",
        "production": "app.config.ProductionConfig"
    }.get(env, "app.config.ProductionConfig")

# ──────────────────────────────────────────────
# 📣 Structured Logging Setup
# ──────────────────────────────────────────────
def setup_logging(debug: bool):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

# ──────────────────────────────────────────────
# 🚀 Main Entrypoint
# ──────────────────────────────────────────────
def main():
    load_dotenv()  # Load .env if present (great for SaaS onboarding)

    # Dynamic config
    config_path = get_config_path()
    debug_flag = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")

    setup_logging(debug_flag)

    # Premium startup log (great for CI/CD logs & support)
    logging.info("=" * 60)
    logging.info("🚀 Launching Starforge Flask SaaS App")
    logging.info(f"🌎 ENV        = {os.getenv('FLASK_ENV', 'production')}")
    logging.info(f"⚙️ CONFIG     = {config_path}")
    logging.info(f"🐞 Debug      = {debug_flag}")
    logging.info(f"🔌 Host:Port  = {host}:{port}")
    logging.info("=" * 60)

    # Setup graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        from app import create_app, socketio
        app = create_app(config_path)

        # 💡 Always define root route for health checks/load balancers!
        @app.route("/")
        def homepage():
            # Optionally, add cache headers, status endpoint, etc. here.
            return render_template("index.html")

        # Pro: Run Flask-SocketIO (real-time fundraising, chat, live updates)
        socketio.run(
            app,
            host=host,
            port=port,
            debug=debug_flag,
            use_reloader=debug_flag,
            allow_unsafe_werkzeug=True,  # Only for local/test!
        )

    except Exception as e:
        logging.error(f"❌ Failed to start Starforge Flask app: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()

