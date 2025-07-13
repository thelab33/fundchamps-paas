# starforge-saas/app/models/transaction.py

from datetime import datetime

from app import db


class Transaction(db.Model):
    """
    Records all payment transactions (donations, sponsorships, refunds, etc).
    Extend for more payment gateways, metadata, or audit trails.
    """
    __tablename__ = 'transactions'

    id           = db.Column(db.Integer, primary_key=True)
    sponsor_id   = db.Column(db.Integer, db.ForeignKey('sponsors.id'), nullable=True)
    amount_cents = db.Column(db.Integer, nullable=False)
    source       = db.Column(db.String(64), default="stripe")  # 'stripe', 'paypal', etc.
    status       = db.Column(db.String(32), default="completed")  # completed, pending, refunded, etc.
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    notes        = db.Column(db.String(255), nullable=True)

    # --- Relationships ---
    sponsor = db.relationship('Sponsor', backref='transactions', lazy=True)

    @property
    def amount_dollars(self):
        """Returns the amount in dollars (float)."""
        return round(self.amount_cents / 100.0, 2) if self.amount_cents else 0.0

    def __repr__(self):
        return f"<Transaction ${self.amount_dollars} ({self.status}) Sponsor: {self.sponsor_id}>"

