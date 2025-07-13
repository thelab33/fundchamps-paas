import os

import openai
from flask import Blueprint, Response, current_app, request

from app.models import SMSLog, db

sms_bp = Blueprint("sms", __name__)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_ai_reply(message, user=None):
    """Fetch a friendly AI response using OpenAI's GPT-4o."""
    openai.api_key = OPENAI_API_KEY
    system_prompt = (
        "You are the friendly digital assistant for Connect ATX Elite youth basketball fundraising. "
        "Respond helpfully and concisely. Suggest how to sponsor or learn more if asked."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            max_tokens=80,
            temperature=0.6,
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        current_app.logger.error(f"[AI SMS] OpenAI error: {e}")
        return (
            "Sorry, our AI is currently unavailable. Please visit connectatxelite.com.",
            str(e),
        )

@sms_bp.route("/webhook", methods=["POST"])
def sms_webhook():
    """
    Receives inbound SMS (from Twilio or similar), passes to AI, logs and replies in XML.
    """
    msg = request.form.get("Body", "").strip()
    from_num = request.form.get("From", "")
    to_num = request.form.get("To", "")

    ai_reply, ai_error = get_ai_reply(msg, user=from_num)

    sms_log = SmsLog(
        from_number=from_num,
        to_number=to_num,
        message_body=msg,
        response_body=ai_reply,
        ai_used=ai_error is None,
        error=ai_error,
    )
    db.session.add(sms_log)
    db.session.commit()

    xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Response>
    <Message>{ai_reply}</Message>
</Response>"""
    return Response(xml, mimetype="application/xml")

