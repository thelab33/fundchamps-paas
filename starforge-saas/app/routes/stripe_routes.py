# app/routes/stripe_routes.py
from flask import Blueprint, request, jsonify, current_app
import stripe
import os

stripe_bp = Blueprint("stripe_bp", __name__, url_prefix="/stripe")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@stripe_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError:
        return "Invalid signature", 400

    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"✅ Payment confirmed: {session['id']}")

    return jsonify(success=True)

@stripe_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout():
    data = request.json or {}
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": data.get("amount", 1000),
                    "product_data": {
                        "name": data.get("description", "Donation"),
                    },
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=data.get("success_url") or request.url_root + "thanks",
            cancel_url=data.get("cancel_url") or request.url_root + "cancelled",
        )
        return jsonify({"id": session.id})
    except Exception as e:
        return jsonify(error=str(e)), 500
