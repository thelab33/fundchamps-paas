#!/usr/bin/env python3
"""
🌟 Enhanced Starforge Audit Script
Includes HTML, CSS, JS, and config misconfiguration checks.
"""

import importlib
import os
import traceback
from pathlib import Path
from rich import print
from rich.console import Console
from rich.panel import Panel
from sqlalchemy import create_engine
from app import create_app

console = Console()

# === CONFIG ===
PROJECT_ROOT = Path(__file__).resolve().parent
APP_DIR = PROJECT_ROOT / "app"
CONFIG_PATH = APP_DIR / "config"
ROUTES_DIR = APP_DIR / "routes"
TEMPLATES_DIR = APP_DIR / "templates"
STATIC_DIR = APP_DIR / "static"
INIT_FILE = APP_DIR / "__init__.py"

required_files = {
    "init": INIT_FILE,
    "routes_dir": ROUTES_DIR,
    "main_route": ROUTES_DIR / "main.py",
    "templates_index": TEMPLATES_DIR / "index.html",
}

expected_config_files = ["__init__.py", "team_config.py", "config.py"]

# === AUDIT FUNCTIONS ===

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
    section("🖼 Template & HTML Validation")
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
    
    # Check for missing aria attributes or incorrect IDs
    for html_file in partials:
        with open(html_file, "r") as f:
            content = f.read()
            if 'aria-' not in content:
                print(f"[red]⚠️ Missing 'aria-' attributes in {html_file}")
            if len(set(content.split('id="'))) != len(content.split('id="')):  # Check for duplicate IDs
                print(f"[red]⚠️ Duplicate 'id' found in {html_file}")


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


def check_database_connection():
    section("🔌 Database Connection Check")
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        try:
            engine = create_engine(db_url)
            with engine.connect() as conn:
                print(f"[green]✅ Successfully connected to database at {db_url}")
        except Exception as e:
            print(f"[red]❌ Database connection failed:[/] {type(e).__name__}: {e}")
            traceback.print_exc()
    else:
        print("[red]⚠️ DATABASE_URL is not set!")


def audit_static_files():
    section("📁 Static Files Check")
    if not STATIC_DIR.exists():
        print(f"[red]❌ No static directory found at {STATIC_DIR}")
        return

    css_files = list(STATIC_DIR.glob("css/*.css"))
    js_files = list(STATIC_DIR.glob("js/*.js"))
    img_files = list(STATIC_DIR.glob("images/*"))

    print(f"[blue]📁 Found {len(css_files)} CSS files in {STATIC_DIR / 'css'}")
    for f in css_files:
        print(f"  - {f.name}")

    print(f"[blue]📁 Found {len(js_files)} JS files in {STATIC_DIR / 'js'}")
    for f in js_files:
        print(f"  - {f.name}")

    print(f"[blue]📁 Found {len(img_files)} image files in {STATIC_DIR / 'images'}")
    for f in img_files:
        print(f"  - {f.name}")


def check_js_validation():
    section("🔧 JavaScript Validation")
    # Check for undefined variables or functions in JavaScript
    js_files = list(STATIC_DIR.glob("js/*.js"))
    for js_file in js_files:
        with open(js_file, "r") as f:
            content = f.read()
            if "undefined" in content:
                print(f"[red]⚠️ Undefined variables or functions in {js_file}")


def check_css_validation():
    section("🎨 CSS Validation")
    # Check for unused or missing CSS classes in HTML files
    css_classes = set()
    for css_file in STATIC_DIR.glob("css/*.css"):
        with open(css_file, "r") as f:
            content = f.read()
            classes = set(content.split(' '))  # Assuming space delimited classes, may need refinement
            css_classes.update(classes)

    for html_file in TEMPLATES_DIR.glob("**/*.html"):
        with open(html_file, "r") as f:
            content = f.read()
            for css_class in css_classes:
                if css_class not in content:
                    print(f"[red]⚠️ Unused CSS class {css_class} in {html_file}")


def check_app_health():
    section("🛠 Application Health Check")
    try:
        app = create_app("app.config.DevelopmentConfig")
        with app.test_client() as c:
            response = c.get("/status")
            if response.status_code == 200:
                print("[green]✅ App status: Healthy")
            else:
                print(f"[red]❌ App status check failed with status: {response.status_code}")
    except Exception as e:
        print(f"[red]❌ App health check failed:[/] {type(e).__name__}: {e}")
        traceback.print_exc()


# === MAIN AUDIT FUNCTION ===
def main():
    print(
        Panel.fit("[bold cyan]🧪 Starforge SaaS App Auditor[/]", style="bold magenta")
    )
    check_required_files()
    check_config_files()
    audit_routes()
    validate_templates()
    check_env_vars()
    check_database_connection()
    audit_static_files()
    check_js_validation()
    check_css_validation()
    check_app_health()


if __name__ == "__main__":
    main()
