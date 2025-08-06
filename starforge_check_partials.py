#!/usr/bin/env python3
"""
Starforge Partial Checker
Scans Jinja2 templates for broken includes, extends, and imports.
"""

import os
import re

TEMPLATE_DIR = "app/templates"
JINJA_EXTENSIONS = (".html", ".jinja", ".jinja2")

INCLUDE_RE = re.compile(r'{%\s*(include|extends|import)\s+["\']([^"\']+)["\']')
missing_files = []

def scan_template(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            match = INCLUDE_RE.search(line)
            if match:
                directive, target = match.groups()
                full_path = os.path.join(TEMPLATE_DIR, target)
                if not os.path.exists(full_path):
                    missing_files.append((file_path, i, directive, target))

def walk_templates():
    for root, _, files in os.walk(TEMPLATE_DIR):
        for file in files:
            if file.endswith(JINJA_EXTENSIONS):
                scan_template(os.path.join(root, file))

def main():
    print("🔍 Scanning templates for missing partials...\n")
    walk_templates()

    if missing_files:
        print("🚨 Broken Jinja references found:")
        for file_path, line_no, directive, target in missing_files:
            print(f"  → {file_path}:{line_no}: `{directive}` missing: `{target}`")
        print("\n❌ Fix or remove the missing includes before build/deploy.\n")
    else:
        print("✅ All includes/extends/imports are valid. You're good to go!")

if __name__ == "__main__":
    main()

