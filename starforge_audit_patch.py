#!/usr/bin/env python3
"""
Starforge SaaS Production Auditor & Auto-Patcher
-------------------------------------------------
- Audits for common Flask/Jinja/Tailwind SaaS issues
- Auto-patches known mistakes (Jinja, static, .bak partials)
- Color-coded output and safety checks
"""
import os
import re
from pathlib import Path

TEMPLATE_DIR = Path('app/templates')
STATIC_DIR = Path('app/static')

def color(msg, code):
    return f"\033[{code}m{msg}\033[0m"

def find_files(pattern, root):
    return list(Path(root).rglob(pattern))

def fix_footer_year(file_path):
    patched = False
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Patch {{ now().year }} -> {{ now.year }}
    new_content = re.sub(r"\{\{\s*now\(\)\.year\s*\}\}", "{{ now.year }}", content)
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(color(f"Patched now().year → now.year in {file_path}", "92"))
        patched = True
    return patched

def patch_bak_includes(file_path):
    patched = False
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Replace .bak, .starforgebak, .starforgenbak includes with .html
    new_content = re.sub(r'include\s+"([^"]+)\.(bak|starforgebak|starforgenbak)"', r'include "\1.html"', content)
    if new_content != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(color(f"Patched includes to .html in {file_path}", "92"))
        patched = True
    return patched

def check_logo_logic(file_path):
    patched = False
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    # Patch old logo logic to flexible logic
    # Looks for src="{{ url_for('static', filename='images/logo.webp') }}" etc
    logo_pattern = r'src="\{\{\s*url_for\(\'static\',\s*filename=(.*?)\)\s*\}\}"'
    if re.search(logo_pattern, content):
        flexible_logo = (
            '{% set logo_src = team.logo if team and team.logo else None %}\n'
            '<img src="{% if logo_src and \'://\' in logo_src %}{{ logo_src }}'
            '{% else %}{{ url_for(\'static\', filename=logo_src or \'images/logo.webp\') }}{% endif %}" '
        )
        # This is a simple version—could be improved to patch in context!
        new_content = re.sub(logo_pattern, flexible_logo, content, count=1)
        if new_content != content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(color(f"Patched flexible logo src in {file_path}", "92"))
            patched = True
    return patched

def audit_templates():
    print(color("\n=== Starforge Template Audit ===", "96"))
    issues = 0
    for tpl in find_files("*.html", TEMPLATE_DIR):
        if tpl.name.endswith((".bak", ".starforgebak", ".starforgenbak")):
            print(color(f"WARNING: Backup template found: {tpl}", "93"))
        if fix_footer_year(tpl):
            issues += 1
        if patch_bak_includes(tpl):
            issues += 1
        if check_logo_logic(tpl):
            issues += 1
    return issues

def remove_unused_backups():
    print(color("\n=== Cleanup Unused Backups ===", "96"))
    removed = 0
    for bak in find_files("*.bak", TEMPLATE_DIR) + find_files("*.starforgebak", TEMPLATE_DIR):
        try:
            os.remove(bak)
            print(color(f"Removed backup: {bak}", "91"))
            removed += 1
        except Exception as e:
            print(color(f"Could not remove {bak}: {e}", "91"))
    return removed

def main():
    print(color("🚦 Running Starforge Production Auditor…", "94"))
    template_issues = audit_templates()
    backups_removed = remove_unused_backups()
    print(color("\n=== Audit Summary ===", "95"))
    if template_issues == 0 and backups_removed == 0:
        print(color("✅ All clear. Templates look production-ready!", "92"))
    else:
        print(color(f"⚠️  {template_issues} issues auto-patched; {backups_removed} backups removed.", "93"))
    print(color("✨ Ready to SaaSify and ship! ✨", "92"))

if __name__ == "__main__":
    main()
