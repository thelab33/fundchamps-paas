# starforge-saas/app/models/user.py

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(db.Model, UserMixin):
    """
    User model for authentication, admin panel, and sponsor login.
    Ready for SaaS multi-role and robust Flask-Login support.
    """
    __tablename__ = "users"

    id             = db.Column(db.Integer, primary_key=True)
    email          = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash  = db.Column(db.String(255), nullable=False)
    is_admin       = db.Column(db.Boolean, default=False)
    is_active      = db.Column(db.Boolean, default=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at     = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Password Security ---
    def set_password(self, password: str):
        """Hashes and sets password for the user."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Checks provided password against stored hash."""
        return check_password_hash(self.password_hash, password)

    # --- Flask-Login Required ---
    def get_id(self):
        """Returns string id for Flask-Login session management."""
        return str(self.id)

    @property
    def is_authenticated(self):
        # Let Flask-Login handle this unless you want custom logic
        return True

    @property
    def display_role(self):
        return "Admin" if self.is_admin else "Sponsor"

    def __repr__(self):
        badge = " [ADMIN]" if self.is_admin else ""
        return f"<User {self.email}{badge}>"

