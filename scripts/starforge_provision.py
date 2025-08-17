#!/usr/bin/env python3
"""
Starforge Tenant Provisioning
Usage:
  python scripts/starforge_provision.py --tenant slug
"""

import argparse, json
from pathlib import Path

TENANTS_DIR = Path("app/tenants")

def provision(tenant: str):
    config_file = TENANTS_DIR / tenant / "config.json"
    if not config_file.exists():
        raise FileNotFoundError(f"No config.json found for tenant {tenant}")

    cfg = json.loads(config_file.read_text())
    print(f"🚀 Provisioning tenant: {tenant}")
    print(f"   Team: {cfg.get('team_name')}")
    print(f"   Fundraising Goal: {cfg.get('fundraising_goal')}")
    # Here: run DB migrations, seed defaults, etc.
    print("✅ Tenant provisioned successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", required=True, help="Tenant slug")
    args = parser.parse_args()
    provision(args.tenant)

