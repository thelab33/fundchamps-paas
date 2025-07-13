from flask import Blueprint, render_template

from app.config.team_config import TEAM_CONFIG

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    """
    Public landing page.
    Pulls from config-based TEAM_CONFIG for safe multi-org SaaS use.
    """
    team = TEAM_CONFIG or {}
    return render_template("index.html", team=team)

