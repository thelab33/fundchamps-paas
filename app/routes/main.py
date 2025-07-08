from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Sponsor, CampaignGoal, Player
from sqlalchemy import func
from app import db
from datetime import datetime

# Define the Blueprint for the main routes
main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    """
    Render the homepage with live fundraising campaign status.
    """
    # Calculate the raised amount from active, approved, and non-deleted sponsors
    raised = db.session.query(func.sum(Sponsor.amount)) \
                       .filter_by(deleted=False, status='approved') \
                       .scalar() or 0

    # Fetch the active campaign goal, defaulting to 10000 if not found
    goal_row = CampaignGoal.query.filter_by(active=True).first()
    goal = goal_row.amount if goal_row else 10000

    # Fetch the 'about' data (for mission, players, etc.)
    about_data = db.session.query(Player).all()  # Fetch players data for the about section

    # Mission statistics (these can be dynamically pulled from your models or database)
    mission_stats = {
        "players": len(about_data),
        "honor_roll": 14,  # Static data; can be fetched dynamically if needed
        "tournaments": 11,  # Static data; can be fetched dynamically if needed
        "years": 4,  # Static data; can be fetched dynamically if needed
    }

    # Stats context
    stats = {
        "raised": raised,
        "goal": goal
    }

    # Pass datetime.now as 'now' so template can use now().year
    return render_template(
        "index.html", 
        stats=stats, 
        raised=raised, 
        goal=goal, 
        about=about_data,
        mission={"stats": mission_stats},
        now=datetime.now
    )

# ==================== SPONSOR SUBMISSION ROUTE ====================

@main_bp.route("/become_sponsor", methods=["POST"])
def become_sponsor():
    """
    Accept sponsor form submission, save to DB, and show thank you.
    """
    name = request.form.get("name", "").strip()
    amount = request.form.get("amount", "").strip()

    if not name or not amount or not amount.isdigit():
        flash("Please provide a valid name and sponsorship amount.", "danger")
        return redirect(url_for("main.home"))

    # Create and save Sponsor
    sponsor = Sponsor(
        name=name,
        amount=int(amount),
        status="pending",  # Or 'approved' if you want instant display
        deleted=False
    )
    db.session.add(sponsor)
    db.session.commit()

    flash(f"Thank you, {name}! Your sponsorship helps Connect ATX Elite shine!", "success")
    return redirect(url_for("main.home"))
