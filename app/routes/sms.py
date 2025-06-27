import os
import openai
from flask import Blueprint, request, Response, current_app, abort
from app.models import SmsLog, db

sms_bp = Blueprint("sms", __name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_ai_reply(message, user=None):
    """Starforge: Use OpenAI to generate a smart reply to an incoming SMS."""
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
                {"role": "user", "content": message}
            ],
            max_tokens=80,
            temperature=0.6,
        )
        return response.choices[0].message.content.strip(), None
    except Exception as e:
        return "Sorry, our AI is currently unavailable. Please visit connectatxelite.com.", str(e)

@sms_bp.route("/webhook", methods=["POST"])
def sms_webhook():
    msg = request.form.get("Body", "").strip()
    from_num = request.form.get("From", "")
    to_num = request.form.get("To", "")

    
    ai_reply, ai_error = get_ai_reply(msg, user=from_num)

    
    sms_log = SmsLog(
        from_number=from_num,
        to_number=to_num,
        message_body=msg,
        response_body=ai_reply,
        ai_used=True if not ai_error else False,
        error=ai_error
    )
    db.session.add(sms_log)
    db.session.commit()

    
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{ai_reply}</Message>
</Response>"""
    return Response(xml, mimetype="application/xml")

