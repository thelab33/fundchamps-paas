from __future__ import annotations

"""
Starforge custom Click CLI

Usage examples:
$ flask starforge audit            # run full audit suite
$ flask starforge audit --model User --limit 20
$ flask starforge seed --demo     # seed demo data
$ flask starforge db-prune        # wipe and reset DB (danger!)
"""

import importlib
import json
from pathlib import Path
from typing import Any, Type

import click
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from app import create_app, db

# ──────────────────────────────────────────────────────────────
# Utility helpers
# ──────────────────────────────────────────────────────────────

console = Console()
BASE_PATH = Path(__file__).resolve().parent


def _load_model(model_name: str) -> Type[Any]:
    """Dynamically load a SQLAlchemy model from app.models."""
    model_module = importlib.import_module(f"app.models.{model_name.lower()}")
    return getattr(model_module, model_name)


# ──────────────────────────────────────────────────────────────
# Main Click group
# ──────────────────────────────────────────────────────────────

@click.group()
def starforge() -> None:
    """Starforge ⚙️ – bespoke dev‑ops tasks for your SaaS."""


# ──────────────────────────────────────────────────────────────
# Audit sub-command
# ──────────────────────────────────────────────────────────────

@starforge.command("audit")
@click.option("--model", default="User", help="SQLAlchemy model to inspect (default: User)")
@click.option("--limit", default=10, help="Max rows to preview in the table")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON instead of a pretty table")
def audit_cmd(model: str, limit: int, as_json: bool) -> None:
    """Run ad-hoc data audits."""
    app = create_app()
    with app.app_context():
        rprint(f"[bold green]✔ Starforge App Ready[/] – [cyan]{app.config['ENV']}[/] | debug={app.debug}")

        Model = _load_model(model)
        total = Model.query.count()
        rows = Model.query.limit(limit).all()

        if as_json:
            data = [
                {c.name: getattr(row, c.name) for c in row.__table__.columns}
                for row in rows
            ]
            console.print_json(json.dumps({"total": total, "rows": data}, default=str))
            return

        table = Table(title=f"{model} snapshot (max {limit}) – total {total}")
        for col in Model.__table__.columns:
            table.add_column(col.name, overflow="fold")
        for row in rows:
            table.add_row(*[str(getattr(row, c.name)) for c in Model.__table__.columns])
        console.print(table)


# ──────────────────────────────────────────────────────────────
# Seed command
# ──────────────────────────────────────────────────────────────

@starforge.command("seed")
@click.option("--demo", is_flag=True, help="Seed faker-generated demo data")
@click.option("--file", type=click.Path(exists=True), help="Seed from JSON/CSV file")
def seed_cmd(demo: bool, file: str | None) -> None:
    """Populate the DB with demo or fixture data."""
    if demo:
        try:
            from app.seeds import seed_demo
        except ModuleNotFoundError:
            rprint("[red]✖ app/seeds.py with seed_demo() missing![/]")
            return
        seed_demo()
        rprint("[green]✔ Demo data seeded.[/]")
    elif file:
        rprint(f"[yellow]⚠️ CSV/JSON import from {file} coming soon ✨[/]")
    else:
        rprint("[red]✖ No seed source specified! Use --demo or --file <path>.[/]")


# ──────────────────────────────────────────────────────────────
# DB Prune command
# ──────────────────────────────────────────────────────────────

@starforge.command("db-prune")
@click.confirmation_option(prompt="This will DELETE all data. Continue?")
def prune_cmd() -> None:
    """Drop all tables and recreate an empty schema (danger!)."""
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        rprint("[bold red]⚠️  Database wiped and recreated![/]")


# Entrypoint for direct CLI usage
if __name__ == "__main__":
    starforge()

