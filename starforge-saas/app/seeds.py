import click
from faker import Faker
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.models import CampaignGoal, Sponsor, User, Team, Player

fake = Faker()


@click.command("seed-demo")
@click.option("--users", default=5, help="Number of demo users to create.")
@click.option("--sponsors", default=8, help="Number of demo sponsors to create.")
@click.option("--players", default=10, help="Number of demo players to create.")
@click.option("--teams", default=1, help="Number of demo teams to create.")
@click.option("--clear", is_flag=True, help="Clear existing demo data before seeding.")
def seed_demo(users, sponsors, players, teams, clear):
    """Populate the DB with realistic demo data."""
    # Import inside the function to avoid circular imports
    from app import create_app

    app = create_app()
    with app.app_context():
        db.create_all()  # autogen tables
        db.create_all()  # 🛠️ autogenerate tables if they don't exist
        if clear:
            click.echo("→ Clearing existing demo data…")
            for model in (Sponsor, User, Player, Team, CampaignGoal):
                model.query.delete()
            db.session.commit()

        # Users
        click.echo(f"→ Seeding {users} users…")
        db.session.add_all(
            [
                User(
                    email=fake.unique.email(),
                    password_hash=generate_password_hash("demo123"),
                    is_admin=False,
                )
                for _ in range(users)
            ]
        )

        # Teams
        click.echo(f"→ Seeding {teams} teams…")
        teams_objs = [
            Team(
                slug=fake.unique.slug(),
                team_name=fake.company(),
                meta_description=fake.sentence(nb_words=6),
            )
            for _ in range(teams)
        ]
        db.session.add_all(teams_objs)

        # Players
        click.echo(f"→ Seeding {players} players…")
        roles = ["Guard", "Forward", "Center"]
        db.session.add_all(
            [
                Player(
                    name=fake.name(),
                    role=fake.random_element(elements=roles),
                    photo_url=fake.image_url(width=200, height=200),
                )
                for _ in range(players)
            ]
        )

        # Sponsors
        click.echo(f"→ Seeding {sponsors} sponsors…")
        db.session.add_all(
            [
                Sponsor(
                    name=fake.company(),
                    email=fake.email(),
                    amount=fake.random_int(min=50, max=2000),
                    message=fake.catch_phrase(),
                    status="approved",
                    deleted=False,
                )
                for _ in range(sponsors)
            ]
        )

        # Campaign goal
        if not CampaignGoal.query.filter_by(active=True).first():
            db.session.add(CampaignGoal(goal_amount=10000, active=True))

        db.session.commit()
        click.echo("✅ Demo data seeded successfully!")
