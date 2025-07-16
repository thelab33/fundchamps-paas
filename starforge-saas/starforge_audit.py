#!/usr/bin/env python3
"""
🌟 Starforge Audit Script
Inspects your Flask SaaS app config, blueprints, templates, and environment for common misconfigurations.
"""

import importlib
import os
import traceback
from pathlib import Path

from rich import print
from rich.console import Console
from rich.panel import Panel

console = Console()

# === CONFIG ===
PROJECT_ROOT = Path(__file__).resolve().parent
APP_DIR = PROJECT_ROOT / "app"
CONFIG_PATH = APP_DIR / "config"
ROUTES_DIR = APP_DIR / "routes"
TEMPLATES_DIR = APP_DIR / "templates"
INIT_FILE = APP_DIR / "__init__.py"

required_files = {
    "init": INIT_FILE,
    "routes_dir": ROUTES_DIR,
    "main_route": ROUTES_DIR / "main.py",
    "templates_index": TEMPLATES_DIR / "index.html",
}

expected_config_files = ["__init__.py", "team_config.py", "config.py"]


def section(title):
    console.rule(f"[bold yellow]{title}")


def check_required_files():
    section("🔍 Required File Structure")
    for label, file in required_files.items():
        if not file.exists():
            print(f"[red]❌ Missing:[/] {file}")
        else:
            print(f"[green]✅ Found:[/] {file}")


def check_config_files():
    section("⚙️ Config File Inspection")
    if not CONFIG_PATH.exists():
        print(f"[red]❌ No config directory at {CONFIG_PATH}")
        return

    for file in expected_config_files:
        f = CONFIG_PATH / file
        if f.exists():
            print(f"[green]✅[/] {file}")
        else:
            print(f"[red]❌[/] Missing: {file}")


def audit_routes():
    section("🧭 Route & Blueprint Check")
    try:
        spec = importlib.util.spec_from_file_location("app", INIT_FILE)
        app_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(app_module)
        app = app_module.create_app("app.config.DevelopmentConfig")
        routes = [str(r.rule) for r in app.url_map.iter_rules()]

        if "/" in routes:
            print("[green]✅ '/' route detected")
        else:
            print("[red]❌ Missing '/' route (homepage)")

        bp_list = list(app.blueprints.keys())
        if "main" in bp_list:
            print("[green]✅ Blueprint 'main' registered")
        else:
            print("[red]❌ Blueprint 'main' not registered")

        print("[blue]📌 Registered Routes:[/]")
        for r in sorted(routes):
            print(f"  • {r}")

    except Exception as e:
        print(f"[red]🔥 Route audit failed:[/] {type(e).__name__}: {e}")
        traceback.print_exc()


def validate_templates():
    section("🖼 Template Availability Check")
    if not TEMPLATES_DIR.exists():
        print("[red]❌ No templates directory found")
        return

    index_file = TEMPLATES_DIR / "index.html"
    if index_file.exists():
        print("[green]✅ index.html found")
    else:
        print("[red]❌ Missing: index.html")

    partials = list(TEMPLATES_DIR.glob("partials/*.html"))
    print(f"[blue]📁 Found {len(partials)} partial templates")
    for p in partials:
        print(f"  - {p.name}")


def check_env_vars():
    section("🌐 Environment Variable Check")
    needed = [
        "FLASK_ENV",
        "FLASK_CONFIG",
        "FLASK_DEBUG",
        "DATABASE_URL",
        "STRIPE_API_KEY",
    ]
    for var in needed:
        val = os.getenv(var)
        if val:
            print(f"[green]✅ {var}[/] = {val}")
        else:
            print(f"[red]⚠️ {var} is unset")


def main():
    print(
        Panel.fit("[bold cyan]🧪 Starforge SaaS App Auditor[/]", style="bold magenta")
    )
    check_required_files()
    check_config_files()
    audit_routes()
    validate_templates()
    check_env_vars()


if __name__ == "__main__":
    main()
