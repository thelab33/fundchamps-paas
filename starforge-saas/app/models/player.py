# app/models/player.py

from __future__ import annotations

import uuid
from datetime import datetime

from app import db


class Player(db.Model):
    """An AAU player on the Connect ATX Elite roster."""
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
        doc="Publicly-safe unique identifier",
    )
    name = db.Column(db.String(120), nullable=False, index=True, doc="Player’s full name")
    role = db.Column(db.String(64), nullable=True, doc="Position or role (e.g., Guard, Forward)")
    photo_url = db.Column(db.String(255), nullable=True, doc="Optional headshot URL")

    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, index=True,
        doc="UTC timestamp when record was created",
    )
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow,
        onupdate=datetime.utcnow, index=True,
        doc="UTC timestamp when record was last updated",
    )

    def __repr__(self) -> str:
        return f"<Player {self.name} ({self.role or 'N/A'})>"

    def as_dict(self) -> dict[str, object]:
        """Serialize to simple dict (for JSON APIs)."""
        return {
            "id": self.id,
            "uuid": self.uuid,
            "name": self.name,
            "role": self.role,
            "photo_url": self.photo_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
