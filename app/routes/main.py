from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from sqlalchemy import func
from app.extensions import db, mail
from app.forms.sponsor_form import SponsorForm
from app.models import CampaignGoal, Sponsor
from flask_mail import Message
from app.config.team_config import TEAM_CONFIG
from typing import Tuple, Dict, Any, Optional, List
from threading import Thread

main_bp = Blueprint("main", __name__)

# ---------- Async Email Sending ----------
def send_async_email(app, msg: Message):
    with app.app_context():
        try:
            mail.send(msg)
            current_app.logger.info(f"Sent email to {msg.recipients}")
        except Exception as e:
            current_app.logger.error(f"Error sending email to {msg.recipients}: {e}")

# ---------- Home / Index ----------
@main_bp.route("/")
def home():
    # -- Team config and campaign goal --
    team = TEAM_CONFIG if 'TEAM_CONFIG' in globals() else {}

    # -- Sponsors data: always pass sorted + total (never undefined!) --
    sponsors_sorted: List[Sponsor] = []
    sponsors_total = 0.0

    try:
        sponsors_sorted = (
            Sponsor.query.filter_by(status="approved", deleted=False)
            .order_by(Sponsor.amount.desc())
            .all() or []
        )
        sponsors_total = sum((s.amount or 0) for s in sponsors_sorted)
    except Exception as e:
        current_app.logger.error(f"[Starforge] Failed fetching sponsors: {e}")

    # -- Spotlight: single sponsor for hero/banner, can be None --
    sponsor = sponsors_sorted[0] if sponsors_sorted else None

    # -- Fundraising stats --
    raised, goal, percent_raised = _get_fundraising_stats()

    # -- Section content: hydrate each section from team or fallback --
    about = _generate_about_section(team)
    impact_stats = _generate_impact_stats(team)
    challenge = _generate_challenge_section(team, impact_stats)
    mission = _generate_mission_section(team, impact_stats)
    stats = _prepare_stats(team, raised, goal, percent_raised)
    challenge["funded"] = f"{percent_raised:.1f}%" if goal else "—"

    features = {
        "digital_hub_enabled": True,  # Toggle from config/db as you grow!
    }

    # --- Render index with all needed context (never missing keys) ---
    return render_template(
        "index.html",
        team=team,
        about=about,
        challenge=challenge,
        mission=mission,
        stats=stats,
        raised=raised,
        goal=goal,
        sponsors_total=sponsors_total,
        sponsors_sorted=sponsors_sorted,
        sponsor=sponsor,
        features=features,
    )

# ---------- Helper Functions ----------
def _prepare_stats(team: Dict[str, Any], raised: float, goal: Optional[float], percent_raised: float) -> Dict[str, Any]:
    return {
        "raised": raised,
        "goal": goal,
        "percent": percent_raised,
        "amount_raised": team.get("amount_raised", raised),
    }

def _generate_about_section(team: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "heading": team.get("about_heading", "About Connect ATX Elite"),
        "text": team.get("about_text", "Family-run AAU program turning East Austin students into honor-roll athletes and leaders."),
        "players": team.get("players", _default_players()),
        "poster": team.get("about_poster", "connect-atx-team.jpg"),
        "cta": {
            "label": team.get("cta_label", "Join Our Champion Circle"),
            "url": "mailto:connectatxelite@gmail.com",
        },
    }

def _default_players() -> list:
    return [
        {"name": "Dame", "role": "Guard"},
        {"name": "Kacen", "role": "Forward"},
        {"name": "Matteo", "role": "Center"},
        {"name": "Trey", "role": "Guard"},
        {"name": "Jackson", "role": "Forward"},
    ]

def _generate_impact_stats(team: Dict[str, Any]) -> list:
    return team.get(
        "impact_stats",
        [{"label": "Players Enrolled", "value": 16}, {"label": "Honor Roll Scholars", "value": 11}]
    )

def _generate_challenge_section(team: Dict[str, Any], impact_stats: list) -> Dict[str, Any]:
    return {
        "heading": team.get("challenge_heading", "The Challenge We Face"),
        "text": team.get("challenge_text", "Despite our passion, we struggle with gym space. Sponsorships make it possible for our youth to train, grow, and succeed."),
        "metrics": [{"label": stat["label"], "value": stat["value"]} for stat in impact_stats],
        "funding_label": team.get("funding_label", "Gym Rental Funding"),
        "funded": None,
        "cta_label": team.get("challenge_cta_label", "Sponsor a Practice"),
        "cta_url": url_for("main.become_sponsor"),
        "testimonial": {
            "text": team.get("challenge_testimonial_text", "Without enough court time, our team can't develop their potential."),
            "author": team.get("challenge_testimonial_author", "Team Parent, Class of 2030"),
            "detail": team.get("challenge_testimonial_detail", "We missed practices last season due to lack of funding for gym rentals. Sponsors make all the difference!"),
        },
    }

def _generate_mission_section(team: Dict[str, Any], impact_stats: list) -> Dict[str, Any]:
    return {
        "heading": team.get("mission_heading", "Our Mission"),
        "text": team.get("mission_text", "Empowering the next generation through basketball, academics, and leadership."),
        "poster": team.get("mission_poster", "connect-atx-team-poster.jpg"),
        "bg_video": team.get("mission_bg_video", "mission-bg.mp4"),
        "story_btn_label": team.get("mission_story_btn_label", "Read Our Story"),
        "share_label": team.get("mission_share_label", "Share Mission"),
        "stats": impact_stats,
        "stories": team.get("mission_stories", _default_mission_stories()),
    }

def _default_mission_stories() -> list:
    return [
        {"text": "“Basketball taught my son confidence and leadership.”", "meta": "Maria R.", "title": "Parent"},
        {"text": "“The team helped me stay on track in school.”", "meta": "David L.", "title": "Class of 2026"},
    ]

def _get_fundraising_stats() -> Tuple[float, Optional[float], float]:
    try:
        raised = db.session.query(func.sum(Sponsor.amount)).filter_by(deleted=False, status="approved").scalar() or 0.0
    except Exception as e:
        current_app.logger.error(f"[Starforge] Failed fetching fundraising totals: {e}")
        raised = 0.0

    goal_row = CampaignGoal.query.filter_by(active=True).first()
    goal = getattr(goal_row, "goal_amount", None) or TEAM_CONFIG.get("fundraising_goal", 10000)
    percent_raised = (raised / goal * 100) if goal else 0.0
    return raised, goal, percent_raised

# ---------- Sponsor Form, Lists, and Static Pages ----------
@main_bp.route("/become-sponsor", methods=["GET", "POST"])
def become_sponsor():
    form = SponsorForm()
    if form.validate_on_submit():
        sponsor = Sponsor(name=form.name.data, email=form.email.data, amount=form.amount.data, status="pending")
        try:
            db.session.add(sponsor)
            db.session.commit()
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
    return Message(
        subject="Thank you for sponsoring Connect ATX Elite!",
        recipients=[email],
        body=f"Hi {name},\n\nThank you for your generous support of Connect ATX Elite!\nWe appreciate your contribution and will keep you updated on our progress.\n\nBest regards,\nConnect ATX Elite Team"
    )

@main_bp.route("/sponsors")
def sponsor_list():
    page = request.args.get("page", 1, type=int)
    per_page = 20
    sponsors_pagination = Sponsor.query.filter_by(status="approved", deleted=False).order_by(Sponsor.amount.desc()).paginate(page=page, per_page=per_page, error_out=False)
    return render_template("sponsor_list.html", sponsors=sponsors_pagination.items, pagination=sponsors_pagination)

@main_bp.route("/calendar")
def calendar():
    return render_template("calendar.html")

@main_bp.route('/sponsor-guide')
def sponsor_guide():
    return render_template('sponsor_guide.html')

@main_bp.route('/player-handbook')
def player_handbook():
    return render_template('player_handbook.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

