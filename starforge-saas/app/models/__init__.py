# app/models/__init__.py — Autoload all models for Starforge SaaS

from app.extensions import db  # ✅ Ensures db is exposed for import

# Core Models
from .campaign_goal import CampaignGoal
from .example import Example
from .player import Player
from .sponsor import Sponsor
from .team import Team
from .user import User
from .transaction import Transaction
from .sms_log import SMSLog

# Optional/experimental
try:
    from .foo_bar import FooBar
    from .foo_model import FooModel
except ImportError:
    pass

