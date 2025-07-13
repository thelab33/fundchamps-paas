"""
Starforge Config Loader 🧬
Exposes both core app configs and team-specific branding config.

Usage (from anywhere):
    from app.config import TEAM_CONFIG, DevelopmentConfig
"""

# ── Load core config classes ──
from .team_config import TEAM_CONFIG, Config, DevelopmentConfig, ProductionConfig

# ── Auto-discoverable for external tools / linters ──
__all__ = [
    "TEAM_CONFIG",
    "Config",
    "DevelopmentConfig",
    "ProductionConfig",
]

