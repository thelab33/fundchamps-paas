import os
from typing import Dict, Any
import stripe
from flask import Blueprint, current_app, jsonify, request
from app.models import Sponsor
from app.extensions import db

stripe_bp = Blueprint("stripe_bp", __name__, url_prefix="/stripe")

# Stripe API key (consider moving to app factory/config)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


@stripe_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    """
    Stripe webhook receiver. Validates signature and dispatches event handlers.
    Handles checkout.session.completed and payment_intent.succeeded events.
    """
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    if not webhook_secret:
        current_app.logger.error("❌ Missing STRIPE_WEBHOOK_SECRET in environment")
        return jsonify(success=False, error="Webhook secret not configured"), 500

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except ValueError:
        current_app.logger.error("❌ Invalid payload received.")
        return jsonify(success=False, error="Invalid payload"), 400
    except stripe.error.SignatureVerificationError:
        current_app.logger.error("❌ Stripe signature verification failed.")
        return jsonify(success=False, error="Invalid signature"), 400
    except Exception as e:
        current_app.logger.error(f"❌ Unknown error processing Stripe webhook: {e}")
        return jsonify(success=False, error="Error processing webhook"), 500

    event_type = event.get("type")
    obj = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        return handle_checkout_session_completed(obj)
    elif event_type == "payment_intent.succeeded":
        return handle_payment_intent_succeeded(obj)
    else:
        current_app.logger.info(f"ℹ️ Unhandled Stripe event type: {event_type}")
        return jsonify(success=True)


def handle_checkout_session_completed(session: Dict[str, Any]):
    """
    Handles 'checkout.session.completed' Stripe event.
    Updates sponsor status to 'approved' and amount paid.
    """
    session_id = session.get("id")
    customer_email = session.get("customer_email")
    amount_total_cents = session.get("amount_total", 0)
    amount_total = float(amount_total_cents) / 100 if amount_total_cents else 0.0

    current_app.logger.info(
        f"✅ Checkout Session Completed — {customer_email} | Session ID: {session_id} | Total Amount: ${amount_total:.2f}"
    )

    if not customer_email:
        current_app.logger.warning("[Stripe Webhook] Missing customer_email in checkout.session.completed")
        return jsonify(success=False, error="Missing customer_email"), 400

    sponsor = Sponsor.query.filter_by(email=customer_email, status="pending").first()
    if not sponsor:
        current_app.logger.warning(f"No pending sponsor found for email {customer_email}.")
        return jsonify(success=True)

    try:
        sponsor.status = "approved"
        sponsor.amount = amount_total
        db.session.commit()
        current_app.logger.info(f"Sponsor {sponsor.name} marked as approved.")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ DB error updating sponsor {sponsor.name}: {e}")
        return jsonify(success=False, error="Database error"), 500

    return jsonify(success=True)


def handle_payment_intent_succeeded(payment_intent: Dict[str, Any]):
    """
    Handles 'payment_intent.succeeded' Stripe event.
    Updates sponsor payment status and amount.
    """
    payment_id = payment_intent.get("id")
    amount_received_cents = payment_intent.get("amount_received", 0)
    amount_received = float(amount_received_cents) / 100 if amount_received_cents else 0.0
    customer = payment_intent.get("customer", "Unknown")

    current_app.logger.info(
        f"💰 PaymentIntent Succeeded — ${amount_received:.2f} | Payment ID: {payment_id} | Customer: {customer}"
    )

    if not payment_id:
        current_app.logger.warning("[Stripe Webhook] Missing payment ID in payment_intent.succeeded")
        return jsonify(success=False, error="Missing payment ID"), 400

    sponsor = Sponsor.query.filter_by(payment_intent=payment_id, status="pending").first()
    if not sponsor:
        current_app.logger.warning(f"No sponsor linked to payment ID {payment_id}.")
        return jsonify(success=True)

    try:
        sponsor.amount = amount_received
        sponsor.status = "approved"
        db.session.commit()
        current_app.logger.info(f"Sponsor {sponsor.name} payment confirmed.")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ DB error confirming payment for sponsor {sponsor.name}: {e}")
        return jsonify(success=False, error="Database error"), 500

    return jsonify(success=True)


@stripe_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """
    Creates a Stripe Checkout Session for payment.

    Expects JSON body with:
    - amount (int): in cents, default 1000 ($10)
    - description (str): product description
    - success_url (str): redirect on success
    - cancel_url (str): redirect on cancel
    - metadata (dict): optional metadata
    """
    data = request.get_json(force=True, silent=True) or {}

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": data.get("amount", 1000),
                        "product_data": {"name": data.get("description", "Donation")},
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=data.get("success_url") or request.url_root + "thanks",
            cancel_url=data.get("cancel_url") or request.url_root + "cancelled",
            metadata=data.get("metadata", {}),
        )
        return jsonify({"id": session.id})
    except stripe.error.StripeError as e:
        current_app.logger.error(f"❌ Stripe session creation failed: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        current_app.logger.error(f"❌ Unexpected error creating checkout session: {e}")
        return jsonify({"error": "Failed to create checkout session"}), 500


# Utility function for logging payment success (optional)
def log_payment_success(email: str, amount: float) -> None:
    sponsor = Sponsor.query.filter_by(email=email).first()
    if sponsor:
        sponsor.amount = amount
        sponsor.status = "approved"
        db.session.commit()
        current_app.logger.info(f"Sponsor {sponsor.name} payment logged successfully.")


# Explicitly export the blueprint for clarity
__all__ = ["stripe_bp"]

