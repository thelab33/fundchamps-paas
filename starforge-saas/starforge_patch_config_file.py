import os


def patch_flask_config():
    config_dir = "app/config"
    flask_config_path = os.path.join(config_dir, "flask_config.py")

    # Check if the flask_config file exists
    if not os.path.exists(flask_config_path):
        print(f"Creating {flask_config_path} as it doesn't exist.")
        with open(flask_config_path, "w") as file:
            # Add a basic configuration structure
            file.write(
                """class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mysecretkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///dev.db'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgresql://localhost/production_db'
"""
            )
        print(f"{flask_config_path} created with default configuration.")
    else:
        print(f"{flask_config_path} already exists.")


if __name__ == "__main__":
    patch_flask_config()
