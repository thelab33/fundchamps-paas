# starforge-saas/app/models/sponsor.py

from datetime import datetime

from app import db


class Sponsor(db.Model):
    """
    Represents an individual or business sponsor for a fundraising campaign.
    Tracks approval, soft deletion, and optional contact/shoutout message.
    """
    __tablename__ = "sponsors"

    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)  # Display/public name
    amount     = db.Column(db.Integer, default=0)           # In cents (not dollars)
    status     = db.Column(db.String(32), default="pending")# pending, approved, rejected
    deleted    = db.Column(db.Boolean, default=False)       # Soft delete for audit/logging

    email      = db.Column(db.String(255), nullable=True)   # For receipts or follow-up
    message    = db.Column(db.String(400), nullable=True)   # Public shoutout/comment

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Relationships ---
    # transactions: see Transaction model's backref

    def is_approved(self):
        """Sponsor is approved and not deleted (safe for leaderboard/public display)."""
        return self.status == "approved" and not self.deleted

    @property
    def amount_dollars(self):
        """Return donation in dollars for display/UI."""
        return self.amount / 100.0 if self.amount else 0.0

    def __repr__(self):
        del_flag = " [DELETED]" if self.deleted else ""
        return f"<Sponsor {self.name} - ${self.amount_dollars:.2f} ({self.status}){del_flag}>"

