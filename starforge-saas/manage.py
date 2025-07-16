#!/usr/bin/env python
"""
manage.py — Alternate Flask entry point
Usage:
    python manage.py
    PORT=5050 FLASK_DEBUG=1 python manage.py
"""

import os
import sys
import signal
import logging
from dotenv import load_dotenv
from app import create_app, socketio


def handle_shutdown(signum, frame):
    """Handles graceful shutdown on receiving a signal."""
    logging.info(f"🛑 Received shutdown signal ({signum}). Exiting gracefully...")
    sys.exit(0)


def get_config():
    """Returns the configuration settings from environment variables."""
    debug_flag = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true", "yes")
    port = int(os.getenv("PORT", 5000))  # Default to 5000 if PORT not set
    host = os.getenv("HOST", "0.0.0.0")  # Default to all interfaces
    return debug_flag, port, host


def setup_logging(debug_flag):
    """Sets up logging configuration."""
    logging.basicConfig(
        level=logging.DEBUG if debug_flag else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def main():
    """Main entry point to launch the Flask app."""
    load_dotenv()  # Load environment variables from a .env file

    # Fetch configuration values
    debug_flag, port, host = get_config()

    # Setup logging
    setup_logging(debug_flag)

    # Log app configuration
    logging.info("=" * 60)
    logging.info("🚀 Launching Starforge Flask app (manage.py)")
    logging.info(f"Debug      = {debug_flag}")
    logging.info(f"Host:Port  = {host}:{port}")
    logging.info("=" * 60)

    # Handle graceful shutdown
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)

    try:
        # Create and run Flask app
        app = create_app()
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


if __name__ == "__main__":
    main()
