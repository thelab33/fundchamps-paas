#!/usr/bin/env python
"""
Connect ATX Elite PaaS SocketIO entry-point.

Usage:
  $ python run.py             # default behavior
  $ python run.py --prod      # load ProductionConfig
  $ python run.py --debug     # enable debugger/reloader
"""

from __future__ import annotations
import os
import sys
import argparse
import traceback
from app import create_app, socketio
import config as cfg_module

# ─── CLI Setup ─────────────────────────────────────────────────────
parser = argparse.ArgumentParser(
    description="Run Connect ATX Elite SocketIO Server"
)
parser.add_argument(
    "--config", "-c", 
    help="Override config class (e.g. config.ProductionConfig)"
)
parser.add_argument(
    "--prod", action="store_true",
    help="Shortcut to config.ProductionConfig"
)
parser.add_argument(
    "--debug", action="store_true",
    help="Force Flask debug & reloader"
)
parser.add_argument(
    "--port", "-p",
    type=int,
    default=int(os.getenv("PORT", 5000)),
    help="Port to bind"
)
args = parser.parse_args()

# ─── Resolve Config ─────────────────────────────────────────────────
env = os.getenv("FLASK_ENV", "development").lower()
dot_cfg = (
    args.config
    or ("config.ProductionConfig" if args.prod else None)
    or os.getenv("FLASK_CONFIG")
    or ("config.DevelopmentConfig" if env == "development" else "config.ProductionConfig")
)
debug_flag = args.debug or os.getenv("FLASK_DEBUG", "0").lower() in {"1", "true"}

# ─── Banner ─────────────────────────────────────────────────────────
print("="*60)
print(f"🚀 Starting Connect ATX Elite SocketIO — ENV={env} DEBUG={debug_flag}")
print(f"Config      : {dot_cfg}")
print(f"Python      : {sys.version.split()[0]}")
print(f"PID         : {os.getpid()}")
print("="*60)

# ─── Launch SocketIO ───────────────────────────────────────────────
try:
    app = create_app(dot_cfg)
    socketio.run(
        app,
        host="0.0.0.0",
        port=args.port,
        debug=debug_flag,
        use_reloader=debug_flag,
        allow_unsafe_werkzeug=True,
    )
except KeyboardInterrupt:
    print("\n✋ Shutdown requested—bye!")
except Exception:
    print("\n💥 Unhandled exception during startup")
    traceback.print_exc()
    sys.exit(1)

