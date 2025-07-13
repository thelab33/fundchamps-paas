# starforge-saas/app/config/__init__.py

# Import Flask config classes for easy access
from .flask_config import Config, DevelopmentConfig, ProductionConfig
from .team_config import TEAM_CONFIG

__all__ = [
    "TEAM_CONFIG",
    "Config",
    "DevelopmentConfig",
    "ProductionConfig",
]
