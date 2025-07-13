# app/extensions.py

from flask_mail import Mail
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

# ─── Extension Instances (unbound) ─────────────────────────────────────────────

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")
mail = Mail()

# ─── Optional: Grouped for cleaner imports elsewhere ─────────────────────────

extensions = {
    "db": db,
    "migrate": migrate,
    "socketio": socketio,
    "mail": mail,
}

