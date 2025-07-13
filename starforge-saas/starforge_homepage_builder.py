#!/usr/bin/env python3

"""
Starforge SaaS Org Homepage Builder
----------------------------------
Scaffold a homepage Jinja template for any org by choosing partials from a YAML recipe!
"""

import sys

import yaml

TEMPLATE = """\
{{% extends "base.html" %}}
{{% block title %}}Home · {{{{ team.team_name if team else 'Your Organization' }}}}{{% endblock %}}

{{% block content %}}
{}
{{% endblock %}}
"""

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Starforge Homepage Builder")
    parser.add_argument('--recipe', '-r', default="default", help="Recipe key from org_homepage_blocks.yaml")
    parser.add_argument('--out', '-o', default="index.html", help="Output file")
    args = parser.parse_args()

    with open("org_homepage_blocks.yaml") as f:
        recipes = yaml.safe_load(f)

    recipe = recipes.get(args.recipe)
    if not recipe:
        print(f"❌ Recipe '{args.recipe}' not found! Edit org_homepage_blocks.yaml.")
        sys.exit(1)

    partial_includes = "\n  ".join(f'{{% include "partials/{p}" %}}' for p in recipe)
    result = TEMPLATE.format(partial_includes)

    with open(f"app/templates/{args.out}", "w") as f:
        f.write(result)

    print(f"✅ Built homepage '{args.out}' using '{args.recipe}' recipe!")

if __name__ == "__main__":
    main()
