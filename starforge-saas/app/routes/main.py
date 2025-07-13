from datetime import datetime
from flask import (
    Blueprint, current_app, flash, redirect, render_template,
    request, url_for,
)
from sqlalchemy import func

from app import db
from app.forms import SponsorForm
from app.models import CampaignGoal, Player, Sponsor

main_bp = Blueprint("main", __name__)


# ─────────────────────────────────────────────────────────────
# 🌐 HOMEPAGE
# ─────────────────────────────────────────────────────────────
@main_bp.route("/")
def home():
    """
    Render the homepage with live fundraising status, goal, player list, and impact stats.
    """
    # 1. Total funds raised
    try:
        raised = (
            db.session.query(func.sum(Sponsor.amount))
            .filter_by(deleted=False, status="approved")
            .scalar()
            or 0
        )
    except Exception as e:
        current_app.logger.warning("Failed to calculate total raised: %s", e)
        raised = 0

    # 2. Active fundraising goal
    goal_row = CampaignGoal.query.filter_by(active=True).first()
    goal = getattr(goal_row, "goal_amount", 10_000) or 10_000

    # 3. Player data for About section
    try:
        about_data = Player.query.all()
    except Exception as e:
        current_app.logger.warning("Failed to load players: %s", e)
        about_data = []

    # 4. Mission impact stats (static for now)
    mission_stats = {
        "players":     len(about_data),
        "honor_roll":  14,
        "tournaments": 11,
        "years":       4,
    }

    return render_template(
        "index.html",
        raised=raised,
        goal=goal,
        about=about_data,
        mission={"stats": mission_stats},
        now=datetime.utcnow,
    )


# ─────────────────────────────────────────────────────────────
# 💌 SPONSOR SUBMISSION
# ─────────────────────────────────────────────────────────────
@main_bp.route("/sponsor", methods=["GET", "POST"])
def sponsor():
    """
    Sponsor form submission (WTForms and legacy POST support).
    """
    form = SponsorForm()

    if form.validate_on_submit():
        try:
            new_sponsor = Sponsor(
                name=form.name.data.strip(),
                email=form.email.data.strip().lower(),
                amount=form.amount.data,
                status="pending",
                deleted=False,
            )
            db.session.add(new_sponsor)
            db.session.commit()

            flash("🎉 Thank you! Your sponsorship info has been submitted.", "success")
            return redirect(url_for("main.home"))

        except Exception as e:
            db.session.rollback()
            current_app.logger.error("Sponsor form error: %s", e)
            flash("⚠️ There was a problem saving your sponsorship. Please try again.", "danger")

    return render_template("sponsor_page.html", form=form)


# ─────────────────────────────────────────────────────────────
# 🔁 LEGACY ROUTE ALIASES (SEO + old links)
# ─────────────────────────────────────────────────────────────
@main_bp.route("/become_sponsor", methods=["POST"])
def become_sponsor_legacy():
    """Support legacy sponsor POST endpoint."""
    return redirect(url_for("main.sponsor"))


@main_bp.route("/index")
def index_alias():
    """Alias for old /index route."""
    return redirect(url_for("main.home"))

