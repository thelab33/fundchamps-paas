# starforge_seed_demo_data.py

from app import create_app, db
from app.models import Sponsor, CampaignGoal, Testimonial  # Add your other models here!

def seed_demo_data():
    app = create_app()
    with app.app_context():
        added = False

        # Seed CampaignGoal (goal for your fundraiser)
        if not CampaignGoal.query.first():
            db.session.add(CampaignGoal(goal_amount=10000, total=0, active=True))
            print("✅ Seeded CampaignGoal")
            added = True

        # Seed Sponsors
        if not Sponsor.query.first():
            sponsors = [
                Sponsor(name="Gold's Gym", amount=500, status="approved"),
                Sponsor(name="Eastside Realty", amount=1000, status="approved"),
                Sponsor(name="Smith Family", amount=150, status="approved"),
                Sponsor(name="Anonymous", amount=50, status="pending"),
            ]
            db.session.add_all(sponsors)
            print("✅ Seeded Sponsors")
            added = True

        # Seed Testimonials
        if not Testimonial.query.first():
            testimonials = [
                Testimonial(author="Coach Angel Rodriguez", text="The brotherhood and discipline we build here creates leaders for life."),
                Testimonial(author="A Grateful Parent", text="This program changed my son's life!"),
                Testimonial(author="Connect ATX Elite player", text="Family means showing up, believing in each other, and making sure no one is left behind."),
            ]
            db.session.add_all(testimonials)
            print("✅ Seeded Testimonials")
            added = True

        # Add more blocks for your other models as needed, eg: Player, User...

        if added:
            db.session.commit()
            print("🎉 Demo data seeded successfully!")
        else:
            print("No demo data was added (tables already have data).")

if __name__ == "__main__":
    seed_demo_data()
