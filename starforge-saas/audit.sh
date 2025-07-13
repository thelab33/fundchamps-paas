#!/usr/bin/env python3
"""
Root-Level Debug & Audit Script for Starforge SaaS
Generates reports in ./reports/ directory, gracefully skipping unavailable tools.
"""

import os
import subprocess
import sys
import shutil


def run_command(name, cmd, outfile):
    """
    Runs a shell command and writes output to outfile. Skips if command not found.
    """
    prog = cmd[0]
    # Allow bash wrappers even if bash is in path
    if prog == 'bash' or shutil.which(prog):
        print(f"==> {name}")
        with open(outfile, "w") as f:
            f.write(f"# Output for {name}\n\n")
            try:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, shell=False)
                if result.returncode != 0:
                    f.write(f"\n# [!] Exit code {result.returncode}\n")
                    print(f"  [!] {name} exited with code {result.returncode}. See {outfile}")
                else:
                    print(f"  [✓] {name} output saved to {outfile}")
            except Exception as e:
                f.write(f"\n# [!] Exception: {e}\n")
                print(f"  [!] {name} exception: {e}. See {outfile}")
    else:
        print(f"  [⇢] Skipped {name}: '{prog}' not found in PATH")
        with open(outfile, "w") as f:
            f.write(f"# Skipped '{name}': command '{prog}' not found in PATH.\n")


def main():
    # Prepare reports directory
    reports_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # Define audit tasks
    tasks = [
        ("Dump Live HTML", ["curl", "-s", "http://127.0.0.1:5000/"], "live_index.html"),
        ("Jinja Syntax Audit", ["jinja2-lint", "app/templates"], "jinja_syntax.txt"),
        ("Broken <img src=> Scan", ["grep", "-R", "src=<img", "-n", "app/templates"], "broken_img_refs.txt"),
        ("Raw Static Reference Audit - href", ["grep", "-R", "href=\"static/\"", "-n", "app/templates"], "static_href_refs.txt"),
        ("Raw Static Reference Audit - src", ["grep", "-R", "src=\"static/\"", "-n", "app/templates"], "static_src_refs.txt"),
        ("Missing url_for in CSS/JS Includes", ["bash", "-lc", "grep -R -E '(href|src)=\"[^\"]+\\.(css|js)\"' -n app/templates | grep -v url_for"], "missing_url_for_assets.txt"),
        ("CSS Fetch Test", ["curl", "-sv", "http://127.0.0.1:5000/static/css/tailwind.min.css"], "css_curl.txt"),
        ("HTML Validation", ["htmlhint", os.path.join(reports_dir, "live_index.html")], "html_validation.txt"),
        ("Security & Lint Sweep", ["bash", "-lc", "ruff check . --exit-zero && bandit -r app -ll -q"], "python_security.txt"),
    ]

    # Execute tasks
    for name, cmd, filename in tasks:
        outfile = os.path.join(reports_dir, filename)
        run_command(name, cmd, outfile)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Aborted by user.")
        sys.exit(1)
