import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_file
from app.models import Sponsor, Transaction, CampaignGoal
from app import db
from app.admin.charts import get_leaderboard_data, get_goal_progress
from app.admin.forms import SponsorForm, EmailForm
import csv, io

admin = Blueprint("admin", __name__, url_prefix="/admin")

# Dashboard
@admin.route("/")
def dashboard():
    sponsors = Sponsor.query.order_by(Sponsor.created_at.desc()).all()
    transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(10).all()
    leaderboard = get_leaderboard_data()
    goal_progress = get_goal_progress()
    return render_template("admin/dashboard.html", sponsors=sponsors, transactions=transactions, leaderboard=leaderboard, goal_progress=goal_progress)

# Sponsor List/Approval
@admin.route("/sponsors")
def sponsors():
    sponsors = Sponsor.query.all()
    return render_template("admin/sponsors.html", sponsors=sponsors)

@admin.route("/sponsors/approve/<int:sponsor_id>", methods=["POST"])
def approve_sponsor(sponsor_id):
    sponsor = Sponsor.query.get_or_404(sponsor_id)
    sponsor.status = "approved"
    db.session.commit()
    flash("Sponsor approved and added to leaderboard!", "success")
    # Optionally ping Slack here!
    return redirect(url_for("admin.sponsors"))

# Export Sponsors
@admin.route("/sponsors/export")
def export_sponsors():
    sponsors = Sponsor.query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Amount", "Email", "Status", "Created"])
    for s in sponsors:
        writer.writerow([s.id, s.name, s.amount, s.email, s.status, s.created_at])
    output.seek(0)
    return send_file(io.BytesIO(output.read().encode()), mimetype="text/csv", as_attachment=True, download_name="sponsors.csv")

# Transactions Table
@admin.route("/transactions")
def transactions():
    txs = Transaction.query.order_by(Transaction.created_at.desc()).all()
    return render_template("admin/transactions.html", transactions=txs)

# Campaign Goals (Edit/View)
@admin.route("/goals", methods=["GET", "POST"])
def goals():
    goal = CampaignGoal.query.first()
    if request.method == "POST":
        goal.amount = request.form["amount"]
        db.session.commit()
        flash("Goal updated!", "success")
        return redirect(url_for("admin.goals"))
    return render_template("admin/goals.html", goal=goal)

# Custom Emails
@admin.route("/emails", methods=["GET", "POST"])
def emails():
    form = EmailForm()
    if form.validate_on_submit():
        # send_email(form.email.data, form.subject.data, form.body.data)
        flash("Email sent!", "success")
        return redirect(url_for("admin.emails"))
    return render_template("admin/emails.html", form=form)

# ... More endpoints as needed!
def notify_slack_new_sponsor(name, amount):
    webhook_url = "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
    msg = {
        "text": f":tada: NEW SPONSOR! {name} gave ${amount} to Connect ATX Elite!",
        "username": "SponsorBot",
        "icon_emoji": ":star2:"
    }
    requests.post(webhook_url, json=msg)
