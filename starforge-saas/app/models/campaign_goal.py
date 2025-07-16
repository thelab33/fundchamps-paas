# app/models/campaign_goal.py

import uuid
from app.extensions import db
from .mixins import TimestampMixin, SoftDeleteMixin


class CampaignGoal(db.Model, TimestampMixin, SoftDeleteMixin):
    """
    Represents a single fundraising goal for a campaign or season.
    Supports soft-delete, timestamps, and easy currency conversions.
    """

    __tablename__ = "campaign_goals"

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        db.String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        index=True,
        doc="Publicly-safe unique identifier",
    )

    # All amounts in cents
    goal_amount = db.Column(
        db.Integer, nullable=False, default=0, doc="Target fundraising goal, in cents"
    )
    total = db.Column(
        db.Integer, nullable=False, default=0, doc="Amount raised so far, in cents"
    )
    active = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        index=True,
        doc="Is this goal currently live?",
    )

    # ── Readable Properties ────────────────────────────────────────────────────

    @property
    def goal_dollars(self) -> float:
        """Goal amount in dollars."""
        return self.goal_amount / 100.0

    @property
    def raised_dollars(self) -> float:
        """Total raised in dollars."""
        return self.total / 100.0

    @property
    def percent_raised(self) -> float:
        """
        Percent of goal achieved, e.g. 42.7
        Returns 0.0 if goal_amount is zero.
        """
        if self.goal_amount:
            return round((self.total / self.goal_amount) * 100, 1)
        return 0.0

    def percent_complete(self) -> int:
        """Integer percent for progress bars (0–100)."""
        return int(self.percent_raised)

    # ── Serialization & Representation ─────────────────────────────────────────

    def as_dict(self) -> dict:
        """
        Serialize key fields for APIs or debugging.
        Excludes internal flags like 'deleted'.
        """
        return {
            "uuid": self.uuid,
            "goal_amount_cents": self.goal_amount,
            "total_raised_cents": self.total,
            "goal_dollars": self.goal_dollars,
            "raised_dollars": self.raised_dollars,
            "percent_raised": self.percent_raised,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self) -> str:
        status = "ACTIVE" if self.active else "INACTIVE"
        return (
            f"<CampaignGoal {self.uuid} "
            f"Goal=${self.goal_dollars:,.2f} "
            f"Raised=${self.raised_dollars:,.2f} "
            f"({self.percent_raised}% – {status})>"
        )
