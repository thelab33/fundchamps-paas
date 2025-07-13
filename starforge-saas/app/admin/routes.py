# app/admin/routes.py
import csv
from io import StringIO

from flask import (
    Blueprint,
    current_app,
    flash,
    make_response,
    redirect,
    render_template,
    url_for,
)
from flask_login import login_required
from sqlalchemy import func

from app.extensions import db
from app.models import CampaignGoal, Sponsor, Transaction

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/")
@login_required
def dashboard():
    """
    Admin dashboard showing KPIs, sponsor list, and transactions.
    """
    try:
        total_raised = (
            db.session.query(func.sum(Sponsor.amount))
            .filter_by(status="approved", deleted=False)
            .scalar()
            or 0
        )
        sponsor_count = Sponsor.query.filter_by(deleted=False).count()
        pending_sponsors = Sponsor.query.filter_by(status="pending", deleted=False).count()
        goal_row = CampaignGoal.query.first()
        goal_amount = getattr(goal_row, "goal_amount", 10000)

        sponsors = Sponsor.query.order_by(Sponsor.created_at.desc()).limit(20).all()
        transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(20).all()

        stats = {
            "total_raised": total_raised,
            "sponsor_count": sponsor_count,
            "pending_sponsors": pending_sponsors,
            "goal_amount": goal_amount,
        }

        return render_template("admin/dashboard.html", stats=stats, sponsors=sponsors, transactions=transactions)

    except Exception as e:
        current_app.logger.error(f"[Admin Dashboard] Error loading stats: {e}")
        flash("Unable to load dashboard data. Please try again later.", "danger")
        return render_template("admin/dashboard.html", stats={}, sponsors=[], transactions=[])


@admin.route("/approve/<int:sponsor_id>", methods=["POST"])
@login_required
def approve_sponsor(sponsor_id):
    sponsor = Sponsor.query.get_or_404(sponsor_id)
    sponsor.status = "approved"
    db.session.commit()
    flash(f"{sponsor.name} has been approved!", "success")
    return redirect(url_for("admin.dashboard"))


@admin.route("/export/payouts")
@login_required
def export_payouts():
    """
    Export all approved sponsors as a CSV file.
    """
    approved_sponsors = Sponsor.query.filter_by(status="approved", deleted=False).all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(["Name", "Email", "Amount", "Status", "Created At"])
    for s in approved_sponsors:
        writer.writerow([s.name, s.email, s.amount, s.status, s.created_at.strftime("%Y-%m-%d %H:%M:%S")])

    response = make_response(si.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=approved_sponsors.csv"
    response.headers["Content-type"] = "text/csv"
    return response

