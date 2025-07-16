from pathlib import Path

# ---- Folder structure ----
folders = [
    "app/admin",
    "app/forms",
    "app/models",
    "app/routes",
    "app/static/css",
    "app/static/js",
    "app/static/images",
    "app/templates/partials",
    "app/templates/macros",
    "logs",
    "migrations/versions",
]
for d in folders:
    Path(d).mkdir(parents=True, exist_ok=True)

# ---- Minimal essential files ----
files = {
    ".gitignore": """
# Python
__pycache__/
*.pyc
instance/
.env
*.sqlite3
# Node/npm
node_modules/
# Logs
logs/
*.log
# OS
.DS_Store
""",
    "requirements.txt": """
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-SocketIO==5.3.6
eventlet==0.35.2
redis==5.0.4
stripe==9.7.0
twilio==9.0.3
openai==1.30.1
sentry-sdk[flask]==2.3.0
Flask-Cors==4.0.1
Flask-Limiter[redis]==3.12.0
gunicorn==22.0.0
gevent==24.2.1
gevent-websocket==0.10.1
black==24.4.2
ipython==8.25.0
python-dotenv==1.0.1
""",
    "run.py": """import os
import sys
from app import create_app, socketio

def main():
    env = os.getenv("FLASK_ENV", "development").lower()
    config_path = os.getenv("FLASK_CONFIG")
    if not config_path:
        config_path = (
            "config.DevelopmentConfig"
            if env == "development"
            else "config.ProductionConfig"
        )
    debug_flag = os.getenv("FLASK_DEBUG", "0").lower() in ("1", "true")
    if "--debug" in sys.argv:
        debug_flag = True
    app = create_app(config_path)
    print(f"🚀 Starting Starforge Flask app in [{env}] mode")
    print(f"Using config: {config_path}")
    print(f"Debug mode: {debug_flag}")
    socketio.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=debug_flag,
        use_reloader=debug_flag,
        allow_unsafe_werkzeug=True,
    )

if __name__ == "__main__":
    main()
""",
    "config.py": """import os
from pathlib import Path
from typing import Type

basedir = Path(__file__).resolve().parent

class _BaseConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///instance/app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    STRIPE_SECRET_KEY: str | None = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY: str | None = os.getenv("STRIPE_PUBLIC_KEY")
    STRIPE_WEBHOOK_SECRET: str | None = os.getenv("STRIPE_WEBHOOK_SECRET")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS: bool = bool(int(os.getenv("MAIL_USE_TLS", 1)))
    MAIL_USERNAME: str | None = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str | None = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER: str = os.getenv(
        "MAIL_DEFAULT_SENDER", "Starforge <noreply@starforge.com>"
    )
    FEATURE_CONFETTI: bool = os.getenv("FEATURE_CONFETTI", "1") == "1"
    FEATURE_AI_THANK_YOU: bool = os.getenv("FEATURE_AI_THANK_YOU", "0") == "1"
    FEATURE_DARK_MODE: bool = os.getenv("FEATURE_DARK_MODE", "1") == "1"
    ENV: str = os.getenv("FLASK_ENV", "production")
    DEBUG: bool = ENV == "development"
    SQLALCHEMY_ECHO: bool = bool(int(os.getenv("SQL_ECHO", 0)))

class DevelopmentConfig(_BaseConfig):
    ENV = "development"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DEV_DATABASE_URL",
        "sqlite:///instance/app.db"
    )

class ProductionConfig(_BaseConfig):
    ENV = "production"
    DEBUG = False

class TestingConfig(_BaseConfig):
    ENV = "testing"
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///instance/test.db"
    )
    WTF_CSRF_ENABLED: bool = False
    STRIPE_SECRET_KEY = "sk_test_123"

def get_config() -> Type[_BaseConfig]:
    env = (os.getenv("FLASK_ENV", "production") or "production").capitalize() + "Config"
    if env not in globals():
        raise RuntimeError(
            f"[config.py] Unknown FLASK_ENV: '{os.getenv('FLASK_ENV')}'. "
            "Use 'development', 'production', or 'testing'."
        )
    return globals()[env]  # type: ignore[index]
""",
    ".env": """
FLASK_ENV=development
SECRET_KEY=super-secret-starforge-key
SQLALCHEMY_DATABASE_URI=sqlite:///instance/app.db
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=youruser
MAIL_PASSWORD=yourpass
MAIL_DEFAULT_SENDER="Starforge <noreply@starforge.com>"
""",
    "app/extensions.py": """from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
socketio = SocketIO(cors_allowed_origins="*")
mail = Mail()
""",
    "app/__init__.py": """from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate, socketio, mail

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_class)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app)
    mail.init_app(app)
    @app.route("/")
    def index():
        return "Starforge SaaS is live! Replace this with Jinja templates."
    return app
""",
    "app/templates/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Starforge Elite</title>
  <meta name="viewport" content="width=device-width,initial-scale=1">
</head>
<body>
  <header>
    <h1>Welcome to Starforge Elite</h1>
    <nav><!-- Navigation here --></nav>
  </header>
  <main>
    {% block content %}Hello, SaaS world!{% endblock %}
  </main>
  <footer>
    <p>&copy; 2025 Starforge Elite</p>
  </footer>
</body>
</html>
""",
    "Dockerfile": """# --- Build Stage ---
FROM node:20-alpine AS build-assets

WORKDIR /app

# Copy package files and install deps
COPY package.json package-lock.json* ./
RUN npm ci

# Copy app static assets and Tailwind config
COPY app/static ./app/static
COPY tailwind.config.js postcss.config.js ./

# Build CSS and JS bundles
RUN npm run build

# --- Final Stage ---
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Flask app code
COPY app ./app
COPY run.py ./

# Copy built static assets from build stage
COPY --from=build-assets /app/app/static ./app/static

# Expose Flask port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
""",
    "package.json": """{
  "name": "starforge-elite-saas",
  "version": "1.0.0",
  "scripts": {
    "dev": "tailwindcss -i ./app/static/css/globals.css -o ./app/static/css/tailwind.min.css --watch",
    "build": "tailwindcss -i ./app/static/css/globals.css -o ./app/static/css/tailwind.min.css"
  },
  "devDependencies": {
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "postcss-import": "^14.1.0",
    "postcss-nested": "^5.0.6",
    "tailwindcss": "^4.1.0"
  }
}
""",
    "postcss.config.js": """module.exports = {
  plugins: [
    require('postcss-import'),
    require('tailwindcss'),
    require('autoprefixer'),
    require('postcss-nested'),
  ],
};
""",
    "tailwind.config.js": """module.exports = {
  darkMode: "class",
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
    "./app/static/css/**/*.css"
  ],
  safelist: [
    "bg-zinc-900", "text-primary", "bg-primary-yellow", "font-bold", "rounded-xl", "shadow-gold-glow"
  ],
  theme: {
    extend: {
      colors: {
        primary: "#facc15",
        "primary-yellow": "#facc15",
        zinc: { 900: "#18181b" }
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography"),
    require("@tailwindcss/aspect-ratio"),
    require("@tailwindcss/line-clamp")
  ]
};
""",
    "app/static/css/globals.css": """@tailwind base;
@tailwind components;
@tailwind utilities;
:root {
  --gold: #facc15;
  --gold-light: #fde68a;
  --black: #18181b;
  --white: #fff;
}
body {
  background: #18181b;
  color: #facc15;
}
""",
}

# --- Write files ---
for path, content in files.items():
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

print("✅ Starforge SaaS scaffold complete! To run:\n")
print("  python3 -m venv .venv && source .venv/bin/activate")
print("  pip install -r requirements.txt")
print("  python run.py")
print("Visit: http://localhost:5000\n")
print("To add more features/partials: copy into app/templates/partials/")
