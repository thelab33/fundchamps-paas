import os
import sys
from types import SimpleNamespace
from jinja2 import Environment, FileSystemLoader, meta, StrictUndefined

TEMPLATE_DIR = "app/templates"  # fix path to your actual templates folder
TEMPLATES = ["index.html", "base.html"]  # add any other templates here

# Minimal fake context with keys your templates expect to avoid false positives
DUMMY_CONTEXT = {
    "team": {},
    "stats": {},
    "announcement": {},
    "funds_raised": 0,
    "fundraising_goal": 0,
    "recent_donors": [],
    "fundraising_deadline": None,
    "confetti_triggered": False,

    # Flask/Jinja globals with dummy placeholders
    "current_user": SimpleNamespace(is_authenticated=False, name="Guest"),
    "_": lambda s: s,  # dummy translation passthrough
    "lang_code": "en",
    "theme": "dark",
    "request": SimpleNamespace(
        url="/",
        base_url="/",
        path="/",
        args={},
        method="GET",
        headers={},
    ),
    "asset_version": "1.0.0",
    "app_env": "development",
    "url_for": lambda endpoint, **kwargs: f"/mocked_url_for/{endpoint}",
}

def audit_template(env, template_name):
    print(f"Auditing {template_name}...")
    try:
        # Load template source
        source = env.loader.get_source(env, template_name)[0]

        # Parse AST to find undeclared variables
        parsed_content = env.parse(source)
        undeclared = meta.find_undeclared_variables(parsed_content)

        # Warn about undeclared variables that are not in dummy context
        undeclared_not_in_context = undeclared - DUMMY_CONTEXT.keys()
        if undeclared_not_in_context:
            print(f"  ⚠️ Undeclared variables not in dummy context: {undeclared_not_in_context}")

        # Render template with StrictUndefined to catch runtime undefined vars
        template = env.get_template(template_name)
        template.render(**DUMMY_CONTEXT)
        print("  ✅ Render successful, no undefined variables at runtime.")
    except Exception as e:
        print(f"  ❌ Error rendering {template_name}: {e}")

def main():
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        undefined=StrictUndefined,
        autoescape=True,
    )

    for tpl in TEMPLATES:
        if not os.path.exists(os.path.join(TEMPLATE_DIR, tpl)):
            print(f"Template {tpl} not found in {TEMPLATE_DIR}")
            continue
        audit_template(env, tpl)

if __name__ == "__main__":
    main()

