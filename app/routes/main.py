from flask import Blueprint, render_template, current_app
# from your_project.services.fundraising import get_fundraising_stats  # Optional hook

# ─── Blueprint Registration ─────────────────────────────────────────────
main_bp = Blueprint("main", __name__)

# ────────────────────────────────────────────────────────────────────────
# 🎯 Home Route – Landing Page with Fundraising Stats
# ------------------------------------------------------------------------
@main_bp.route("/")
def home():
    """
    Render the homepage with fundraising campaign status.
    Replace the hardcoded values with live data from Stripe, DB, or API.
    """
    # 💰 Fundraising Metrics (replace with real-time logic)
    raised = 0      # Example: get_fundraising_stats()["raised"]
    goal = 10000    # Example: get_fundraising_stats()["goal"]

    stats = {
        "raised": raised,
        "goal": goal
    }

    # 📄 Render the landing page with campaign stats
    return render_template("index.html", stats=stats, raised=raised, goal=goal)

