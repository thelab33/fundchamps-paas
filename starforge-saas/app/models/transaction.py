# app/models/transaction.py — Payment transaction records with timestamps and helpers
import uuid
from app.extensions import db
from .mixins import TimestampMixin


class Transaction(db.Model, TimestampMixin):
    """
    Records every payment event (donations, sponsorships, refunds, etc).
    Includes automatic created/updated timestamps via TimestampMixin.
    """

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
        doc="Publicly-safe unique identifier for this transaction",
    )
    sponsor_id = db.Column(
        db.Integer,
        db.ForeignKey("sponsors.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc="Associated sponsor (if any)",
    )
    amount_cents = db.Column(
        db.Integer, nullable=False, doc="Transaction amount in cents"
    )
    source = db.Column(
        db.String(64),
        nullable=False,
        default="stripe",
        doc="Payment gateway/source (e.g., stripe, paypal)",
    )
    status = db.Column(
        db.String(32),
        nullable=False,
        default="completed",
        doc="Transaction status (completed, pending, refunded, failed)",
    )
    notes = db.Column(
        db.String(255), nullable=True, doc="Optional metadata or human-readable notes"
    )

    # Relationship back to Sponsor
    sponsor = db.relationship(
        "Sponsor",
        backref=db.backref("transactions", lazy="dynamic"),
        passive_deletes=True,
    )

    @property
    def amount_dollars(self) -> float:
        """Return the transaction amount in dollars."""
        return round(self.amount_cents / 100.0, 2)

    def as_dict(self) -> dict:
        """
        Serialize transaction to a dict for JSON APIs or auditing.
        """
        return {
            "id": self.id,
            "uuid": self.uuid,
            "sponsor_id": self.sponsor_id,
            "amount_cents": self.amount_cents,
            "amount_dollars": self.amount_dollars,
            "source": self.source,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        return (
            f"<Transaction {self.uuid} ${self.amount_dollars}"
            f" status={self.status} sponsor={self.sponsor_id}>"
        )
