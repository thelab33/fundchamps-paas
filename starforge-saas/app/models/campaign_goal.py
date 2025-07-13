from datetime import datetime

from app import db


class CampaignGoal(db.Model):
    """
    Represents a single fundraising goal for a campaign or season.
    Can be extended for multi-goal or stretch goal campaigns.
    """
    __tablename__ = "campaign_goals"

    id = db.Column(db.Integer, primary_key=True)
    # Target goal in cents (e.g., 250000 = $2,500.00)
    goal_amount = db.Column(db.Integer, nullable=False)
    # Total raised so far in cents
    total = db.Column(db.Integer, default=0, nullable=False)
    # Indicates if this goal is currently live
    active = db.Column(db.Boolean, default=True, nullable=False)

    # ── Timestamps ──────────────────────────────────────────────────────────
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        doc="UTC timestamp when the goal was created",
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        doc="UTC timestamp when the goal was last updated",
    )

    # --- Properties & Helpers ---
    @property
    def amount(self) -> int:
        """Alias for goal_amount (backward compatibility)."""
        return self.goal_amount

    @property
    def raised(self) -> int:
        """Amount raised in cents."""
        return self.total or 0

    @property
    def goal_dollars(self) -> float:
        """Returns goal amount in dollars."""
        return (self.goal_amount or 0) / 100.0

    @property
    def raised_dollars(self) -> float:
        """Returns raised amount in dollars."""
        return self.raised / 100.0

    @property
    def percent_raised(self) -> float:
        """Returns percent raised (e.g., 42.5)."""
        if self.goal_amount:
            return round((self.raised / self.goal_amount) * 100, 1)
        return 0.0

    def percent_complete(self) -> int:
        """Returns percent complete as integer for progress bars."""
        return int(self.percent_raised)

    def __repr__(self) -> str:
        status = "ACTIVE" if self.active else "INACTIVE"
        return (
            f"<CampaignGoal ${self.goal_dollars:,.2f} "
            f"(Raised: ${self.raised_dollars:,.2f}, {self.percent_raised}% - {status})>"
        )

