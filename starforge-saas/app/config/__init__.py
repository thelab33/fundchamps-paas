import os
"""Centralized config loader for Starforge SaaS."""

from app.config.config import DevelopmentConfig, ProductionConfig

# Optional: add TestingConfig, StagingConfig, etc., as needed
try:
    from app.config.config import TestingConfig
except ImportError:
    TestingConfig = None

# Try importing team config
try:
    from app.config.team_config import TEAM_CONFIG
except ImportError:
    TEAM_CONFIG = {}
    # Optional: Log with Flask logger if app context, or print otherwise
    try:
        from flask import current_app
        current_app.logger.warning("⚠️ TEAM_CONFIG not found, using empty config.")
    except Exception:
        print("⚠️ TEAM_CONFIG not found, using empty config.")

# Master config map
CONFIGS = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
if TestingConfig:
    CONFIGS["testing"] = TestingConfig

# Team-specific config is always available
CONFIGS["team_config"] = TEAM_CONFIG

def get_config(env: str = None):
    """
    Returns the config class based on environment variable or argument.
    Defaults to 'development' if not specified or unknown.
    """
    env = env or os.getenv("FLASK_ENV", "development")
    return CONFIGS.get(env, DevelopmentConfig)

# Shorthand for quick import elsewhere
config = get_config()
team_config = TEAM_CONFIG

