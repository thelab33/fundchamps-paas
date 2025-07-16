from flask import (
    Blueprint,
    current_app,
    render_template,
    redirect,
    url_for,
    flash,
    request,
)
from sqlalchemy import func
from app.extensions import db, mail
from app.forms.sponsor_form import SponsorForm
from app.models import CampaignGoal, Sponsor
from flask_mail import Message
from app.config import TEAM_CONFIG
from typing import Tuple, Dict, Any, Optional
from threading import Thread

main_bp = Blueprint("main", __name__)


def send_async_email(app, msg):
    """Send email asynchronously to avoid blocking HTTP requests."""
    with app.app_context():
        try:
            mail.send(msg)
            current_app.logger.info(f"Sent email to {msg.recipients}")
        except Exception as e:
            current_app.logger.error(f"Error sending email to {msg.recipients}: {e}")


@main_bp.route("/")
def home():
    """Render the SaaS homepage with dynamic team sections and fundraising stats."""
    team = TEAM_CONFIG or {}

    about = _generate_about_section(team)
    impact_stats = _generate_impact_stats(team)
    challenge = _generate_challenge_section(team, impact_stats)
    mission = _generate_mission_section(team, impact_stats)

    raised, goal, percent_raised = _get_fundraising_stats()
    stats = {
        "raised": raised,
        "goal": goal,
        "percent": percent_raised,
        "amount_raised": team.get("amount_raised", raised),
    }

    challenge["funded"] = f"{percent_raised:.1f}%" if goal else "—"

    return render_template(
        "index.html",
        team=team,
        about=about,
        challenge=challenge,
        mission=mission,
        stats=stats,
        raised=raised,
        goal=goal,
    )


def _generate_about_section(team: Dict[str, Any]) -> Dict[str, Any]:
    """Build the About section content."""
    return {
        "heading": team.get("about_heading", "About Connect ATX Elite"),
        "text": team.get(
            "about_text",
            "Family-run AAU program turning East Austin students into honor-roll athletes and leaders.",
        ),
        "players": team.get(
            "players",
            [
                {"name": "Dame", "role": "Guard"},
                {"name": "Kacen", "role": "Forward"},
                {"name": "Matteo", "role": "Center"},
                {"name": "Trey", "role": "Guard"},
                {"name": "Jackson", "role": "Forward"},
            ],
        ),
        "poster": team.get("about_poster", "connect-atx-team.jpg"),
        "cta": {
            "label": team.get("cta_label", "Join Our Champion Circle"),
            "url": "mailto:connectatxelite@gmail.com",
        },
    }


def _generate_impact_stats(team: Dict[str, Any]) -> list:
    """Build impact statistics list."""
    return team.get(
        "impact_stats",
        [
            {"label": "Players Enrolled", "value": 16},
            {"label": "Honor Roll Scholars", "value": 11},
        ],
    )


def _generate_challenge_section(team: Dict[str, Any], impact_stats: list) -> Dict[str, Any]:
    """Build challenge section content."""
    return {
        "heading": team.get("challenge_heading", "The Challenge We Face"),
        "text": team.get(
            "challenge_text",
            "Despite our passion, we struggle with gym space. Sponsorships make it possible for our youth to train, grow, and succeed.",
        ),
        "metrics": [{"label": stat["label"], "value": stat["value"]} for stat in impact_stats],
        "funding_label": team.get("funding_label", "Gym Rental Funding"),
        "funded": None,  # to be populated later
        "cta_label": team.get("challenge_cta_label", "Sponsor a Practice"),
        "cta_url": url_for("main.become_sponsor"),
        "testimonial": {
            "text": team.get(
                "challenge_testimonial_text",
                "Without enough court time, our team can't develop their potential.",
            ),
            "author": team.get("challenge_testimonial_author", "Team Parent, Class of 2030"),
            "detail": team.get(
                "challenge_testimonial_detail",
                "We missed practices last season due to lack of funding for gym rentals. Sponsors make all the difference!",
            ),
        },
    }


def _generate_mission_section(team: Dict[str, Any], impact_stats: list) -> Dict[str, Any]:
    """Build mission section content."""
    return {
        "heading": team.get("mission_heading", "Our Mission"),
        "text": team.get(
            "mission_text",
            "Empowering the next generation through basketball, academics, and leadership.",
        ),
        "poster": team.get("mission_poster", "connect-atx-team-poster.jpg"),
        "bg_video": team.get("mission_bg_video", "mission-bg.mp4"),
        "story_btn_label": team.get("mission_story_btn_label", "Read Our Story"),
        "share_label": team.get("mission_share_label", "Share Mission"),
        "stats": impact_stats,
        "stories": team.get(
            "mission_stories",
            [
                {
                    "text": "“Basketball taught my son confidence and leadership.”",
                    "meta": "Maria R.",
                    "title": "Parent",
                },
                {
                    "text": "“The team helped me stay on track in school.”",
                    "meta": "David L.",
                    "title": "Class of 2026",
                },
            ],
        ),
    }


def _get_fundraising_stats() -> Tuple[float, Optional[float], float]:
    """
    Calculate fundraising totals from the DB.

    Returns:
        raised: total amount raised
        goal: fundraising goal amount
        percent_raised: percent of goal raised
    """
    try:
        raised = (
            db.session.query(func.sum(Sponsor.amount))
            .filter_by(deleted=False, status="approved")
            .scalar()
        ) or 0.0
    except Exception as e:
        current_app.logger.error(f"[Starforge] Failed fetching fundraising totals: {e}")
        raised = 0.0

    goal_row = CampaignGoal.query.filter_by(active=True).first()
    goal = getattr(goal_row, "goal_amount", None) or TEAM_CONFIG.get("fundraising_goal", 10000)

    percent_raised = (raised / goal * 100) if goal else 0.0

    return raised, goal, percent_raised


@main_bp.route("/become-sponsor", methods=["GET", "POST"])
def become_sponsor():
    """Sponsor sign-up with form validation and async email notification."""
    form = SponsorForm()
    if form.validate_on_submit():
        sponsor = Sponsor(
            name=form.name.data,
            email=form.email.data,
            amount=form.amount.data,
            status="pending",
        )
        try:
            db.session.add(sponsor)
            db.session.commit()
            # Async email send to avoid blocking response
            Thread(target=send_async_email, args=(current_app._get_current_object(), _create_thank_you_msg(form.name.data, form.email.data))).start()
            flash("Thank you for your sponsorship! We'll be in touch soon.", "success")
            return redirect(url_for("main.home"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Sponsor form submission error: {e}")
            flash("Something went wrong. Please try again.", "danger")
    elif request.method == "POST":
        flash("Please correct the errors in the form.", "warning")

    return render_template("become_sponsor.html", form=form)


def _create_thank_you_msg(name: str, email: str) -> Message:
    """Create the thank-you email message."""
    return Message(
        subject="Thank you for sponsoring Connect ATX Elite!",
        recipients=[email],
        body=(
            f"Hi {name},\n\n"
            "Thank you for your generous support of Connect ATX Elite!\n"
            "We appreciate your contribution and will keep you updated on our progress.\n\n"
            "Best regards,\n"
            "Connect ATX Elite Team"
        ),
    )


@main_bp.route("/sponsors")
def sponsor_list():
    """Display paginated list of approved sponsors, ordered by amount descending."""
    page = request.args.get("page", 1, type=int)
    per_page = 20  # Paginate 20 per page

    sponsors_pagination = Sponsor.query.filter_by(status="approved", deleted=False).order_by(Sponsor.amount.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template("sponsor_list.html", sponsors=sponsors_pagination.items, pagination=sponsors_pagination)

