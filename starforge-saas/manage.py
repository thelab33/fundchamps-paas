#!/usr/bin/env python3
import os
import sys
import traceback

from app import create_app, socketio

def main():
    env = os.getenv("FLASK_ENV", "development").lower()
    cfg_path = os.getenv("FLASK_CONFIG") or (
        "config.DevelopmentConfig" if env == "development" else "config.ProductionConfig"
    )

    debug = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true") or "--debug" in sys.argv

    print("=" * 60)
    print(f"🚀 Launching Starforge Flask ({env})")
    print(f"🔧 Config Path: {cfg_path}")
    print(f"🐞 Debug Mode: {debug}")
    print(f"📦 PID: {os.getpid()} | Python: {sys.version}")
    print("=" * 60)

    try:
        app = create_app(cfg_path)
        socketio.run(
            app,
            host="0.0.0.0",
            port=int(os.getenv("PORT", 5000)),
            debug=debug,
            use_reloader=debug,
        )
    except Exception:
        print("❌ Flask failed to start:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
