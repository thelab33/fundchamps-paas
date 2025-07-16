from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Sponsor, CampaignGoal, Player
from app.forms import SponsorForm
from sqlalchemy import func
from app import db
from datetime import datetime

main_bp = Blueprint("main", __name__)

# ==================== HOMEPAGE ====================
@main_bp.route("/")
def home():
    """
    Render the homepage with live fundraising campaign status.
    """
    raised = (
        db.session.query(func.sum(Sponsor.amount))
        .filter_by(deleted=False, status="approved")
        .scalar()
        or 0
    )

    goal_row = CampaignGoal.query.filter_by(active=True).first()
    goal = getattr(goal_row, "goal_amount", 10000)

    about_data = db.session.query(Player).all()

    mission_stats = {
        "players": len(about_data),
        "honor_roll": 14,
        "tournaments": 11,
        "years": 4,
    }

    stats = {"raised": raised, "goal": goal}

    return render_template(
        "index.html",
        stats=stats,
        raised=raised,
        goal=goal,
        about=about_data,
        mission={"stats": mission_stats},
        now=datetime.now,
    )


# ==================== SPONSOR POST (Legacy Manual Submission) ====================
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

    sponsor = Sponsor(
        name=name,
        amount=int(amount),
        status="pending",
        deleted=False,
    )
    db.session.add(sponsor)
    db.session.commit()

    flash(f"Thank you, {name}! Your sponsorship helps Connect ATX Elite shine!", "success")
    return redirect(url_for("main.home"))


# ==================== SPONSOR FORM (WTForms Route) ====================
@main_bp.route("/sponsor", methods=["GET", "POST"])
def sponsor():
    """
    Display and process the full WTForm-based sponsor form.
    """
    form = SponsorForm()
    if form.validate_on_submit():
        new_sponsor = Sponsor(
            name=form.name.data,
            amount=form.amount.data,
            status="pending",
            deleted=False,
        )
        db.session.add(new_sponsor)
        db.session.commit()

        flash("Sponsor info submitted! Thank you for supporting the team.", "success")
        return redirect(url_for("main.home"))

    return render_template("sponsor_page.html", form=form)

