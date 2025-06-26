from flask import Blueprint, request, Response

sms_bp = Blueprint("sms", __name__)

@sms_bp.route("/webhook", methods=["POST"])
def sms_webhook():
    # Example: Twilio webhook
    msg = request.form.get("Body", "")
    # Do something with the SMS message here
    return Response(f"<Response><Message>Echo: {msg}</Message></Response>", mimetype="application/xml")
