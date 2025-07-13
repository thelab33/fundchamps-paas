import stripe
from flask import Blueprint, current_app, jsonify, request

webhooks_bp = Blueprint("webhooks", __name__)

@webhooks_bp.route("/webhook/stripe", methods=["POST"])
def stripe_webhook():
    """
    Stripe webhook endpoint.
    Handles 'checkout.session.completed' and 'payment_intent.succeeded' events.
    """
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    endpoint_secret = current_app.config.get("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        current_app.logger.error(f"[Stripe Webhook] Verification failed: {e}")
        return jsonify(success=False, error=str(e)), 400

    event_type = event.get("type")
    data_object = event["data"]["object"]

    if event_type == "checkout.session.completed":
        session_id = data_object.get("id")
        customer_email = data_object.get("customer_email")
        current_app.logger.info(f"✅ Checkout completed for {customer_email} (session: {session_id})")

        # Optional: Add logic to match sponsor with session/payment

    elif event_type == "payment_intent.succeeded":
        payment_id = data_object.get("id")
        amount = data_object.get("amount_received") / 100.0
        current_app.logger.info(f"💰 PaymentIntent succeeded: ${amount:.2f} (ID: {payment_id})")

    else:
        current_app.logger.info(f"[Stripe Webhook] Unhandled event type: {event_type}")

    return jsonify(success=True)

