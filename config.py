import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add more config (Stripe keys, etc) as needed

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
