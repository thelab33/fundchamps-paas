import click
from faker import Faker
from werkzeug.security import generate_password_hash
from app.extensions import db
from app.models import CampaignGoal, Sponsor, User, Team, Player

# ✅ 1. Define CLI group at the top — always!
from flask.cli import AppGroup
starforge = AppGroup("starforge")

fake = Faker()

@starforge.command("seed-demo")
@click.option("--users", default=5, help="Number of demo users to create.")
@click.option("--sponsors", default=8, help="Number of demo sponsors to create.")
@click.option("--players", default=10, help="Number of demo players to create.")
@click.option("--teams", default=1, help="Number of demo teams to create.")
@click.option("--clear", is_flag=True, help="Clear existing demo data before seeding.")
def seed_demo_cmd(users, sponsors, players, teams, clear):
    """
    Populate the database with realistic demo data for a FundChamps onboarding or live demo.
    """
    from app import create_app
    app = create_app()
    with app.app_context():
        db.create_all()

        if clear:
            click.secho("→ Clearing existing demo data…", fg="yellow")
            for model in (Sponsor, User, Player, Team, CampaignGoal):
                model.query.delete()
            db.session.commit()

        # Teams (seed first for relationships)
        click.secho(f"→ Seeding {teams} team(s)…", fg="green")
        team_objs = []
        for _ in range(teams):
            t = Team(
                slug=fake.unique.slug(),
                team_name=fake.company(),
                meta_description=fake.sentence(nb_words=8),
            )
            db.session.add(t)
            team_objs.append(t)
        db.session.commit()

        # Users
        click.secho(f"→ Seeding {users} user(s)…", fg="green")
        db.session.add_all([
            User(
                email=fake.unique.email(),
                password_hash=generate_password_hash("demo123"),
                is_admin=False,
                team_id=team_objs[0].id if team_objs else None,
            ) for _ in range(users)
        ])

        # Players
        click.secho(f"→ Seeding {players} player(s)…", fg="green")
        roles = ["Guard", "Forward", "Center"]
        db.session.add_all([
            Player(
                name=fake.name(),
                role=fake.random_element(elements=roles),
                photo_url=fake.image_url(width=200, height=200),
                team_id=team_objs[0].id if team_objs else None,
            ) for _ in range(players)
        ])

        # Sponsors
        click.secho(f"→ Seeding {sponsors} sponsor(s)…", fg="green")
        db.session.add_all([
            Sponsor(
                name=fake.company(),
                email=fake.unique.email(),
                amount=fake.random_int(min=50, max=2500),
                message=fake.catch_phrase(),
                status="approved",
                deleted=False,
                team_id=team_objs[0].id if team_objs else None,
            ) for _ in range(sponsors)
        ])

        # Campaign goal (one per team, future proof for multi-team FundChamps SaaS)
        for team in team_objs:
            if not CampaignGoal.query.filter_by(team_id=team.id, active=True).first():
                db.session.add(CampaignGoal(goal_amount=10000, active=True, team_id=team.id))
        db.session.commit()

        click.secho("✅ Demo data seeded successfully!", fg="bright_green", bold=True)

# At the end of cli.py — so it can be imported into your app/__init__.py and registered!

