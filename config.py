import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

