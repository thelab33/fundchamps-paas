# starforge-saas/app/config/flask_config.py

import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")

    @staticmethod
    def get_db_uri():
        db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../data/app.db")
        )
        print(f"[config/flask_config.py] Using SQLite DB at: {db_path}")
        return f"sqlite:///{db_path}"

    SQLALCHEMY_DATABASE_URI = get_db_uri.__func__()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ALLOW_ORIGINS = "*"
    LIMITER_REDIS_URL = "memory://"
    LOG_LEVEL = "INFO"
    LOG_FILE = None

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    LOG_FILE = "development.log"

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "INFO"
    LOG_FILE = "/var/log/connect_atx_elite/app.log"
    CORS_ALLOW_ORIGINS = "https://yourproductiondomain.com"
    LIMITER_REDIS_URL = "redis://localhost:6379"
