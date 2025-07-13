import os

PATCHED_ENV_PY = """\
import logging
from logging.config import fileConfig
import sys

from alembic import context

config = context.config

# Setup logging via Alembic's .ini
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# Get Flask app
try:
    from flask import current_app
    app = current_app._get_current_object()
    logger.info("✅ Using Flask app context for Alembic migrations.")
except Exception as e:
    logger.error("❌ Could not access Flask app context.")
    logger.error("Make sure to run commands like `flask db upgrade` or `flask db migrate`.")
    sys.exit(1)

# Import db from app
try:
    from app import db
except ImportError as e:
    logger.error("❌ Could not import `db` from your app: %s", e)
    sys.exit(1)

def get_engine():
    try:
        return db.get_engine(app)  # Flask-SQLAlchemy < 3
    except (AttributeError, TypeError):
        return db.engine  # Flask-SQLAlchemy >= 3

def get_engine_url():
    engine = get_engine()
    url_str = str(engine.url)
    masked = url_str.replace(engine.url.password or '', '****') if engine.url.password else url_str
    logger.info(f"🔗 Using DB: {masked}")
    return engine.url.render_as_string(hide_password=False).replace('%', '%%')

config.set_main_option('sqlalchemy.url', get_engine_url())

# Import models
try:
    import app.models  # noqa
except ImportError as e:
    logger.error("❌ Could not import models: %s", e)
    sys.exit(1)

def get_metadata():
    if hasattr(db, 'metadatas'):  # Flask-SQLAlchemy 3+
        return db.metadatas.get(None)
    return db.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    logger.info(f"🚀 Running Alembic offline migrations on {url}")
    context.configure(
        url=url,
        target_metadata=get_metadata(),
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("🧘 No schema changes detected.")

    connectable = get_engine()
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            process_revision_directives=process_revision_directives,
            **app.extensions['migrate'].configure_args,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""

def patch_env_py():
    env_path = os.path.join("migrations", "env.py")
    if not os.path.exists(env_path):
        print("❌ migrations/env.py not found.")
        return

    with open(env_path, "w") as f:
        f.write(PATCHED_ENV_PY)

    print("✅ Patched migrations/env.py with Starforge-compatible migration config.\n")

if __name__ == "__main__":
    patch_env_py()
