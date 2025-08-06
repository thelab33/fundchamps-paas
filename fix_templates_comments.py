#!/usr/bin/env python3
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "app" / "templates"

# Match files we render through Jinja
GLOBS = ["**/*.html", "**/*.jinja", "**/*.jinja2"]

# Strategy:
# - If a file has NO '{#' but has '#}', treat all '#}' as stray and remove them.
# - Also collapse sequences like '#} #} #}' even if a file does have some valid comments.
# - Make a .bak backup next to each changed file.

def fix_text(p: Path, text: str) -> str:
    original = text

    # 1) Collapse repeated closers anywhere
    text = re.sub(r"(#}\s*){2,}", "", text)

    # 2) If the file has zero comment openings, remove any closers
    if "{#" not in text and "#}" in text:
        text = text.replace("#}", "")

    # 3) If we still have orphan closers on lines that never opened, strip them per-line
    def strip_orphan(line: str) -> str:
        if "{#" not in line and "#}" in line:
            return line.replace("#}", "")
        return line
    text = "\n".join(strip_orphan(line) for line in text.splitlines())

    return text if text != original else original

def main():
    changed = 0
    files = []
    for g in GLOBS:
        files += list(TEMPLATES.glob(g))

    for p in sorted(files):
        try:
            s = p.read_text(encoding="utf-8")
        except Exception:
            continue
        new = fix_text(p, s)
        if new != s:
            bak = p.with_suffix(p.suffix + ".bak")
            bak.write_text(s, encoding="utf-8")
            p.write_text(new, encoding="utf-8")
            changed += 1
            print(f"✓ fixed {p.relative_to(ROOT)} (backup: {bak.name})")

    if not changed:
        print("No stray '#}' issues found.")
    else:
        print(f"Done. Patched {changed} file(s).")

if __name__ == "__main__":
    main()
