from flask import Blueprint, render_template, current_app

from app.models import Sponsor, CampaignGoal  
from sqlalchemy import func
from app import db

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    """
    Starforge: Render the homepage with live fundraising campaign status.
    Replace the hardcoded values with live DB, Stripe API, or external metrics.
    """
    
    
    raised = db.session.query(func.sum(Sponsor.amount)).filter_by(deleted=False, status='approved').scalar() or 0
    goal_row = CampaignGoal.query.filter_by(active=True).first()
    goal = goal_row.amount if goal_row else 10000

    stats = {
        "raised": raised,
        "goal": goal
    }

    
    
    

    
    
    
    

    return render_template("index.html", stats=stats, raised=raised, goal=goal)

