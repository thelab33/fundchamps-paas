
"""
Starforge: Blueprint import hub.
All route blueprints are imported here for easy registration in your Flask app.
"""

from .main import main_bp
from .api import api_bp
from .sms import sms_bp


try:
    from app.admin.routes import admin as admin_bp
except ImportError:
    admin_bp = None  




