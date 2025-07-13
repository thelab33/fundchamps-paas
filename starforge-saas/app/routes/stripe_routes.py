import os

import stripe
from flask import Blueprint, current_app, jsonify, request

from app import db, socketio
from app.models import CampaignGoal, Sponsor, Transaction

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
DOMAIN = os.getenv("DOMAIN", "http://localhost:5000")

stripe_bp = Blueprint("stripe_bp", __name__)


@stripe_bp.post("/api/donate")
def create_checkout():
    """
    Create Stripe Checkout session for sponsorships/donations.
    Expects JSON: { "name": "John Doe", "amount": "50.00", "email": "john@example.com" }
    """
    data = request.get_json(force=True)
    try:
        amount_cents = int(float(data["amount"]) * 100)
        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card", "us_bank_account", "link"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": amount_cents,
                        "product_data": {"name": f"Sponsorship — {data['name']}"},
                    },
                    "quantity": 1,
                }
            ],
            customer_email=data.get("email"),
            metadata={"sponsor_name": data["name"]},
            success_url=f"{DOMAIN}?success=true&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{DOMAIN}?canceled=true",
        )
        return jsonify({"url": session.url})
    except Exception as e:
        current_app.logger.error(f"[Stripe] Checkout error: {e}")
        return jsonify({"error": "Unable to start payment session."}), 400


@stripe_bp.post("/stripe/webhook")
def stripe_webhook():
    """
    Stripe webhook endpoint for payment events.
    On 'checkout.session.completed', records the donation and notifies via SocketIO.
    """
    payload = request.data
    sig = request.headers.get("stripe-signature")
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig, secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        current_app.logger.error(f"[Stripe] Webhook error: {e}")
        return "Invalid payload", 400

    if event["type"] == "checkout.session.completed":
        s = event["data"]["object"]
        amount = s["amount_total"] // 100
        name = s["metadata"].get("sponsor_name", "Anonymous")

        # Create Sponsor record
        sponsor = Sponsor(name=name, amount=amount, status="approved")
        db.session.add(sponsor)

        # Update goal, if present
        goal = CampaignGoal.query.filter_by(active=True).first()
        if goal:
            goal.total = (goal.total or 0) + amount

        # Log transaction
        txn = Transaction(amount_cents=amount * 100)
        db.session.add(txn)
        db.session.commit()

        # Real-time broadcast (for live updates on front end)
        socketio.emit(
            "new_sponsor",
            {
                "name": name,
                "amount": amount,
                "goal_total": goal.total if goal else None,
            },
        )

    return "OK", 200

