# app/seeds.py
from __future__ import annotations

import random

from faker import Faker
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import CampaignGoal, Sponsor, User  # adjust if needed

fake = Faker()

def seed_demo():
    app = create_app()
    with app.app_context():
        # ── Users ─────────────────────────────
        print("→ Seeding users")
        users = [
            User(
                name=fake.name(),
                email=fake.unique.email(),
                password_hash=generate_password_hash("demo123")  # Secure hash
            ) for _ in range(5)
        ]
        db.session.add_all(users)

        # ── Sponsors ──────────────────────────
        print("→ Seeding sponsors")
        sponsors = [
            Sponsor(
                name=fake.company(),
                amount=random.randint(100, 1500),
                message=fake.catch_phrase(),
                status="approved"
            ) for _ in range(8)
        ]
        db.session.add_all(sponsors)

        # ── Campaign Goal (create if missing) ─
        if not CampaignGoal.query.first():
            db.session.add(CampaignGoal(goal_amount=10000))

        db.session.commit()
        print("✅ Demo data seeded!")

