# app/models/user.py

from __future__ import annotations
import uuid
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db
from app.models.mixins import TimestampMixin


class User(db.Model, UserMixin, TimestampMixin):
    """
    User model for authentication, admin panel, and sponsor login.
    Supports Flask-Login and timestamp auditing.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
        doc="Publicly safe unique identifier",
    )
    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
        doc="User's email address",
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False,
        doc="Hashed password",
    )
    is_admin = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
        doc="Admin flag",
    )
    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
        doc="Account enabled flag",
    )

    def __repr__(self) -> str:
        role = "Admin" if self.is_admin else "User"
        return f"<User {self.email} ({role})>"

    # ─── Password helpers ─────────────────────────────────────────────────────
    def set_password(self, password: str) -> None:
        """Hash & store the given plaintext password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify the given plaintext password against stored hash."""
        return check_password_hash(self.password_hash, password)

    # ─── Flask-Login ──────────────────────────────────────────────────────────
    def get_id(self) -> str:
        """Return the canonical ID for Flask-Login."""
        return str(self.id)

    @property
    def display_role(self) -> str:
        """A human-friendly name for this user's role."""
        return "Admin" if self.is_admin else "Sponsor"
