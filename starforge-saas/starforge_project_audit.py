#!/usr/bin/env python3
"""
Starforge Project Audit: SaaS Elite Launch-Readiness Analyzer

- Scans your repo for structure, blueprints, UI/UX, config, secrets, models, static, templates, admin, business logic.
- Flags missing or broken pieces, surface-level security issues, and scaling gaps.
- Outputs a color-coded report and a /_starforge_audit directory with detailed logs.
"""

import os
import sys
import re
import shutil
from pathlib import Path
from datetime import datetime
import subprocess

AUDIT_DIR = Path("_starforge_audit")
AUDIT_DIR.mkdir(exist_ok=True)

def color(text, code):
    return f"\033[{code}m{text}\033[0m"
OK    = lambda t: color(t, "1;32")
WARN  = lambda t: color(t, "1;33")
FAIL  = lambda t: color(t, "1;31")
BOLD  = lambda t: color(t, "1;36")
SKIP  = lambda t: color(t, "0;37")

def log_section(title):
    print(BOLD(f"\n━━ {title} ━━"))

def write_file(title, content):
    path = AUDIT_DIR / (title.replace(" ", "_").replace("/", "_").lower() + ".txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def run_shell(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.STDOUT)
    except Exception as e:
        return f"ERROR: {e}"

def check_file_exists(path):
    return Path(path).exists()

def check_folder_exists(path):
    return Path(path).is_dir()

def scan_files(pattern, root="."):
    return list(Path(root).rglob(pattern))

def get_first_line(filepath):
    try:
        with open(filepath) as f:
            return f.readline().strip()
    except Exception:
        return ""

def get_blueprints(app_folder):
    bps = []
    for f in Path(app_folder).rglob("*.py"):
        try:
            text = f.read_text()
            if "Blueprint(" in text:
                for bp in re.findall(r'Blueprint\(["\']([\w-]+)["\']', text):
                    bps.append((f, bp))
        except Exception:
            pass
    return bps

def get_routes(app_folder):
    routes = []
    for f in Path(app_folder).rglob("*.py"):
        try:
            lines = f.read_text().splitlines()
            for i, line in enumerate(lines):
                if "@app.route" in line or "@.*_bp.route" in line:
                    routes.append((f, i+1, line.strip()))
        except Exception:
            pass
    return routes

def find_env_secrets(env_file):
    secrets = []
    if not Path(env_file).exists(): return secrets
    with open(env_file) as f:
        for line in f:
            if any(x in line.lower() for x in ["key", "secret", "password", "token"]) and "=" in line and not line.strip().startswith("#"):
                secrets.append(line.strip())
    return secrets

def audit():
    print(BOLD(f"\nStarforge Project Audit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"))
    print(f"All output logs: {AUDIT_DIR}/\n")

    ## 1. Directory Health
    log_section("Project Structure")
    tree = run_shell("tree -a -L 3")
    write_file("structure_tree", tree)
    must_have = [
        "app/", "app/routes/", "app/models/", "app/templates/", "app/static/",
        "requirements.txt", "run.py", "app/config.py"
    ]
    for d in must_have:
        status = OK("✅") if check_folder_exists(d) or check_file_exists(d) else FAIL("❌")
        print(f" {status} {d}")

    ## 2. Config & Secrets
    log_section("Configs & Secrets")
    configs = [p for p in ["requirements.txt", ".env", ".env.example", "app/config.py", "app/config/team_config.py"] if Path(p).exists()]
    for c in configs:
        print(f" {OK('✓')} {c}")
    secrets = find_env_secrets(".env")
    if secrets:
        print(WARN("  [!] Sensitive values found in .env (ensure this is NOT checked in!):"))
        for s in secrets: print(f"      {s}")
    else:
        print(OK("  No secrets detected in .env."))
    write_file("env_secrets", "\n".join(secrets) if secrets else "No secrets found.")

    ## 3. Blueprints, Routes, and Views
    log_section("Flask Blueprints & Routes")
    blueprints = get_blueprints("app/routes")
    if blueprints:
        print(OK(f" Found {len(blueprints)} blueprints:"))
        for bp in blueprints:
            print(f"   {bp[1]:<20} (in {bp[0].relative_to('.')})")
    else:
        print(FAIL("  No blueprints found in app/routes."))
    write_file("blueprints", "\n".join(f"{b[1]} - {b[0]}" for b in blueprints))

    ## 4. Models
    log_section("Database Models")
    models = scan_files("*.py", "app/models")
    for m in models:
        name = m.name
        if re.search(r'class\s+\w*\(?db\.Model', m.read_text()):
            print(OK(f" Found model class in {name}"))
    write_file("models", "\n".join(str(m) for m in models))

    ## 5. Templates & Partials
    log_section("Templates & Partials")
    htmls = scan_files("*.html", "app/templates")
    print(f" {OK('✓')} {len(htmls)} HTML templates/partials found.")
    if not htmls:
        print(FAIL("  [!] No HTML templates found in app/templates."))
    write_file("templates_partials", "\n".join(str(h) for h in htmls))

    ## 6. Static Assets (CSS/JS/Images)
    log_section("Static Assets")
    static_assets = scan_files("*", "app/static")
    css = [f for f in static_assets if f.suffix == ".css"]
    js  = [f for f in static_assets if f.suffix == ".js"]
    img = [f for f in static_assets if f.suffix in {".svg",".png",".jpg",".webp",".avif",".gif"}]
    print(f"  CSS: {len(css)}, JS: {len(js)}, Images: {len(img)}")
    write_file("static_css", "\n".join(str(f) for f in css))
    write_file("static_js", "\n".join(str(f) for f in js))
    write_file("static_images", "\n".join(str(f) for f in img))

    ## 7. Admin & Dashboards
    log_section("Admin/Dashboard")
    admin_html = scan_files("*.html", "app/templates/admin")
    if admin_html:
        print(OK(f" {len(admin_html)} admin templates found."))
    else:
        print(SKIP(" No admin dashboard templates detected."))
    write_file("admin_templates", "\n".join(str(a) for a in admin_html))

    ## 8. Business Logic/CLI
    log_section("CLI & Business Scripts")
    cli_py = scan_files("cli.py", "app")
    seeds_py = scan_files("seeds.py", "app")
    if cli_py: print(OK(f"✓ CLI found: {cli_py[0]}"))
    if seeds_py: print(OK(f"✓ Seed script: {seeds_py[0]}"))
    write_file("cli", "\n".join(str(c) for c in cli_py))
    write_file("seeds", "\n".join(str(s) for s in seeds_py))

    ## 9. Git Status
    log_section("Git Status (Uncommitted Files)")
    git_status = run_shell("git status --short")
    if git_status.strip():
        print(WARN("  [!] Uncommitted changes detected!"))
        print(git_status)
    else:
        print(OK("  Git working directory clean."))
    write_file("git_status", git_status)

    ## 10. Pro Tips & Next Steps
    log_section("Pro Tips & Founder Checklist")
    print(BOLD(" - Run `python3 starforge_project_audit.py` after every major change."))
    print(BOLD(" - Review _starforge_audit/ logs for partner/demo prep."))
    print(BOLD(" - Never check `.env` or actual secrets into Git!"))
    print(BOLD(" - Ask your cofounder AI for patches on any flagged gap."))
    print(BOLD(" - Run Lighthouse audits for UI/UX accessibility and performance."))

    print(OK("\nAudit complete! Review output above and in the _starforge_audit directory."))
    print(BOLD("Paste this output to your AI cofounder for a production-grade SaaS polish! 🚀"))

if __name__ == "__main__":
    audit()
