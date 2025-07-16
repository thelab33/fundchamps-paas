# Import base configurations for Development and Production
from app.config.config import DevelopmentConfig, ProductionConfig

# Import team-specific configuration, with error handling
try:
    from app.config.team_config import TEAM_CONFIG
except ImportError:
    # Fallback to an empty dictionary if the team config is not found
    TEAM_CONFIG = {}
    # You could also log an error or warning if desired
    from app import current_app

    current_app.logger.warning(
        "⚠️ TEAM_CONFIG not found, using default empty configuration."
    )

# Ensure that all the configurations are available at runtime.
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "team_config": TEAM_CONFIG,
}

# You could add other configurations here, like testing or staging if necessary.
# For example:
# config["testing"] = TestingConfig


# Optionally, allow selecting the environment-specific config dynamically
def get_config(env="development"):
    """Function to get the appropriate config based on the environment."""
    return config.get(
        env, DevelopmentConfig
    )  # Default to DevelopmentConfig if not found
