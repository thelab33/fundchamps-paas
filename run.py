#!/usr/bin/env python3
"""
    🚀 Starforge Flask SaaS Entrypoint
    ----------------------------------
    This script handles app creation, configuration, graceful shutdown, and real-time server launch.
    Elite-polished for both production and local development environments.
"""

import os
import sys
import signal
import logging
from dotenv import load_dotenv
from app import create_app  # Ensure this import is correct
from flask_socketio import SocketIO

# ──────────────────────────────────────────────
# 🛑 Graceful Shutdown Handler
# ──────────────────────────────────────────────
def handle_shutdown(signum, frame):
    """
    Handles graceful shutdown when a termination signal is received.
    Logs the shutdown process and exits cleanly.
    """
    logging.info(f"🛑 Received shutdown signal ({signum}). Exiting gracefully...")
    sys.exit(0)

# ──────────────────────────────────────────────
# ⚙️ Config Class Path Resolver
# ──────────────────────────────────────────────
def get_config_path() -> str:
    """
    Resolves the configuration path based on environment variables.
    Returns the appropriate config class for the current environment (development, testing, production).
    """
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
def setup_logging(debug: bool):
    """
    Configures the logging setup. Sets the logging level based on the debug flag.
    The log format includes timestamp, log level, and the message.
    """
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

# ──────────────────────────────────────────────
# 🚀 Main Entrypoint
# ──────────────────────────────────────────────
def main():
    """
    Main entrypoint for launching the Starforge Flask app.
    This function sets up the environment, logging, and starts the application with SocketIO support.
    """
    load_dotenv()  # Load environment variables from .env file, great for SaaS onboarding

    # Dynamically resolve the configuration path based on the environment
    config_path = get_config_path()
    
    # Set the debug flag and port/host settings from environment variables
    debug_flag = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")

    # Set up logging based on the debug flag
    setup_logging(debug_flag)

    # Log important startup information (great for CI/CD & support)
    logging.info("=" * 60)
    logging.info("🚀 Launching Starforge Flask SaaS App")
    logging.info(f"🌎 ENV        = {os.getenv('FLASK_ENV', 'production')}")
    logging.info(f"⚙️ CONFIG     = {config_path}")
    logging.info(f"🐞 Debug      = {debug_flag}")
    logging.info(f"🔌 Host:Port  = {host}:{port}")
    logging.info("=" * 60)

    # Set up signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        # Create the Flask app based on the resolved config path
        app = create_app(config_path)
        
        # Initialize SocketIO with the Flask app
        socketio = SocketIO(app, async_mode='eventlet')

        # Run the Flask-SocketIO application with Eventlet
        socketio.run(
            app,
            host=host,
            port=port,
            debug=debug_flag,
            use_reloader=debug_flag,  # Use the reloader in development mode
        )

    except Exception as e:
        logging.error(f"❌ Failed to start Starforge Flask app: {e}", exc_info=True)
        sys.exit(1)

# ──────────────────────────────────────────────
# Check if the script is being run directly
# ──────────────────────────────────────────────
if __name__ == "__main__":
    main()

