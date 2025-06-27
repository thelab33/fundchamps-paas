# app/routes/stripe_routes.py
import os, stripe, json, time
from flask import Blueprint, current_app as app, request, jsonify, url_for
from app import db, socketio
from app.models import Sponsor, Transaction, CampaignGoal

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
DOMAIN        = os.getenv("DOMAIN", "http://localhost:5000")

stripe_bp = Blueprint("stripe_bp", __name__)

# --- 1. create checkout session -------------------------------------------
@stripe_bp.post("/api/donate")
def create_checkout():
    data = request.get_json(force=True)
    amount_cents = int(float(data["amount"]) * 100)

    session = stripe.checkout.Session.create(
        mode="payment",
        payment_method_types=["card","us_bank_account","link"],  # Apple/Google Pay auto-enabled
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": amount_cents,
                "product_data": {"name": f"Sponsorship — {data['name']}"},
            },
            "quantity": 1,
        }],
        customer_email=data.get("email"),
        metadata={"sponsor_name": data["name"]},
        success_url=f"{DOMAIN}?success=true&session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{DOMAIN}?canceled=true",
    )
    return jsonify({"url": session.url})

# --- 2. webhook -----------------------------------------------------------
@stripe_bp.post("/stripe/webhook")
def stripe_webhook():
    payload  = request.data
    sig      = request.headers.get("stripe-signature")
    secret   = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return "Invalid payload", 400

    if event["type"] == "checkout.session.completed":
        s      = event["data"]["object"]
        amount = s["amount_total"] // 100
        name   = s["metadata"]["sponsor_name"]

        # ---- DB write -----------------------------------------------------
        sponsor = Sponsor(name=name, amount=amount, status="approved")
        db.session.add(sponsor)

        goal = CampaignGoal.query.filter_by(active=True).first()
        if goal:
            goal.total += amount

        txn = Transaction(amount_cents=amount*100)
        db.session.add(txn)
        db.session.commit()

        # ---- real-time broadcast -----------------------------------------
        socketio.emit("new_sponsor", {
            "name": name,
            "amount": amount,
            "goal_total": goal.total if goal else None,
        })

    return "OK", 200
