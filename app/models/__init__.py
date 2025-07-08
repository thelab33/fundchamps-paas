# Importing all necessary models from their respective modules
from app import db
from .sponsor import Sponsor
from .campaign_goal import CampaignGoal
from .example import Example
from .foo_model import FooModel
from .sms_log import SmsLog
from .foo_bar import FooBar
from .transaction import Transaction
from .player import Player  # Make sure to import the Player model

# The __all__ declaration defines what gets imported when using 'from module import *'
# This makes sure only the listed models are imported, keeping the module namespace clean.
__all__ = [
    'Transaction',  # A transaction-related model, likely for financial or data-related records
    'FooBar',       # Another business-specific model
    'SmsLog',       # Model for SMS logs, probably for tracking communications
    'db',           # SQLAlchemy's database instance for working with the database
    'Sponsor',      # The Sponsor model, relevant for your fundraising platform
    'CampaignGoal', # Model that holds the campaign goal details
    'Example',      # Placeholder or sample model
    'FooModel',     # Another specific model, potentially for handling Foo objects
    'Player'        # Make sure Player is included in the __all__ list
]
