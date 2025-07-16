from __future__ import annotations
import importlib
import json
from pathlib import Path
from typing import Any, Type

import click
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from app import db  # Keep this (safe to import)

# Initialize console for rich printing
console = Console()
BASE_PATH = Path(__file__).resolve().parent


def _load_model(model_name: str) -> Type[Any]:
    """Dynamically load the model class from app.models."""
    model_module = importlib.import_module(f"app.models.{model_name.lower()}")
    return getattr(model_module, model_name)


@click.group()
def starforge() -> None:
    """Starforge ⚙️ – DevOps toolkit for Connect ATX Elite SaaS."""


@starforge.command("audit")
@click.option("--model", default="User", help="Model to inspect")
@click.option("--limit", default=10, help="How many records to fetch")
@click.option("--json", "as_json", is_flag=True, help="Output raw JSON")
def audit_cmd(model: str, limit: int, as_json: bool) -> None:
    """
    Audits a model by fetching records, supports JSON output.
    """
    from app import create_app  # Lazy import here

    app = create_app()

    with app.app_context():
        rprint(f"[green]✔ Loaded:[/] {model} | ENV: [cyan]{app.config['ENV']}[/]")

        Model = _load_model(model)
        total = Model.query.count()
        rows = Model.query.limit(limit).all()

        if as_json:
            # Return data in JSON format
            data = [
                {col.name: getattr(row, col.name) for col in row.__table__.columns}
                for row in rows
            ]
            console.print_json(json.dumps({"total": total, "rows": data}, default=str))
        else:
            # Display in tabular format using rich
            table = Table(title=f"{model} (Top {limit}) — Total: {total}")
            for col in Model.__table__.columns:
                table.add_column(col.name, overflow="fold")
            for row in rows:
                table.add_row(
                    *[str(getattr(row, col.name)) for col in Model.__table__.columns]
                )
            console.print(table)


@starforge.command("seed")
@click.option("--demo", is_flag=True, help="Seed demo content (faker)")
@click.option("--file", type=click.Path(exists=True), help="Seed from CSV/JSON file")
def seed_cmd(demo: bool, file: str | None) -> None:
    """
    Seed the database with demo data or data from a file.
    """
    if demo:
        try:
            from app.seeds import seed_demo

            seed_demo()
            rprint("[green]✔ Demo data seeded.[/]")
        except ModuleNotFoundError:
            rprint("[red]✖ No seed_demo() found in app/seeds.py[/]")
    elif file:
        rprint(f"[yellow]⚠️ File import from {file} coming soon.[/]")
    else:
        rprint("[red]✖ Please use --demo or --file to seed data.[/]")


@starforge.command("db-prune")
@click.confirmation_option(prompt="⚠️ This will wipe ALL data. Are you sure?")
def prune_cmd() -> None:
    """
    Prune (reset) the database. Deletes all data.
    """
    from app import create_app  # Lazy import here

    app = create_app()

    with app.app_context():
        db.drop_all()
        db.create_all()
        rprint("[bold red]⚠️ Database wiped and reset![/]")


if __name__ == "__main__":
    starforge()
