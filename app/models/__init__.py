# app/models/__init__.py — Autoload all models & mixins for Starforge SaaS

from app.extensions import db  # ✅ Expose db for use in mixins and models

# Mixins
from .mixins import TimestampMixin, SoftDeleteMixin

# Core Models
from .campaign_goal import CampaignGoal
from .example import Example
from .player import Player
from .sponsor import Sponsor
from .team import Team
from .transaction import Transaction
from .sms_log import SMSLog
from .user import User

# Optional/experimental
try:
    # Try to import something real, or just:
    pass
except ImportError:
    pass

__all__ = [
    "db",
    # Mixins
    "TimestampMixin",
    "SoftDeleteMixin",
    # Core models
    "CampaignGoal",
    "Example",
    "Player",
    "Sponsor",
    "Team",
    "Transaction",
    "SMSLog",
    "User",
    # Experimental
]
