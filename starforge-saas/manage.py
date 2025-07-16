#!/usr/bin/env python3
"""
manage.py — Flask CLI utility for database, shell, etc.
Usage:
    python manage.py db upgrade
    python manage.py shell
"""

from flask.cli import FlaskGroup
from app import create_app

app = create_app()
cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()

