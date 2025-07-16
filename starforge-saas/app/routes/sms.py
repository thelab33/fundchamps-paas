import os
from datetime import datetime
from typing import Tuple, Optional

import openai
from flask import Blueprint, Response, current_app, request
from markupsafe import escape
from app.extensions import db
from app.models import SMSLog


sms_bp = Blueprint("sms", __name__, url_prefix="/sms")


def get_ai_reply(message: str) -> Tuple[str, Optional[str]]:
    """
    Generate an AI response for inbound SMS using OpenAI.

    Returns:
        reply_text (str): The AI-generated reply text.
        error_str (Optional[str]): Error message if any, else None.
    """
    api_key = (
        current_app.config.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY", "").strip()
    )
    if not api_key:
        current_app.logger.warning("[AI SMS] Missing OpenAI API key")
        return (
            "Sorry, our AI assistant is temporarily offline. Please visit connectatxelite.com.",
            "Missing OpenAI API key",
        )

    openai.api_key = api_key

    system_prompt = current_app.config.get(
        "OPENAI_SYSTEM_PROMPT",
        "You are the friendly digital assistant for Connect ATX Elite youth basketball fundraising. "
        "Be brief, helpful, and positive. Share how to sponsor, donate, or support the team if asked.",
    )

    model = current_app.config.get("OPENAI_MODEL", "gpt-4o")

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            max_tokens=100,
            temperature=0.6,
        )
        reply_text = response.choices[0].message.content.strip()
        current_app.logger.info(f"[AI SMS] Generated reply: {reply_text}")
        return reply_text, None

    except Exception as ex:
        current_app.logger.error(f"[AI SMS] OpenAI API error: {ex}", exc_info=True)
        return (
            "Sorry, our AI helper is currently unavailable. Please visit connectatxelite.com.",
            str(ex),
        )


@sms_bp.route("/webhook", methods=["POST"])
def sms_webhook() -> Response:
    """
    Twilio-style SMS webhook endpoint.

    Receives inbound SMS, generates AI reply, logs interaction to DB, and returns TwiML XML.
    """
    incoming = request.form or {}
    body = incoming.get("Body", "").strip()
    from_number = incoming.get("From", "").strip()
    to_number = incoming.get("To", "").strip()

    if not body:
        current_app.logger.warning(f"[SMS] Empty message received from {from_number}")
        xml_resp = "<Response><Message>Empty message received. Please send a valid query.</Message></Response>"
        return Response(xml_resp, mimetype="application/xml")

    # Optional: Add rate limiting or abuse prevention here

    reply, error = get_ai_reply(body)

    sms_log = SMSLog(
        from_number=from_number,
        to_number=to_number,
        message_body=body,
        response_body=reply,
        ai_used=(error is None),
        error=error,
        timestamp=datetime.utcnow(),
    )

    try:
        db.session.add(sms_log)
        db.session.commit()
        current_app.logger.info(f"[SMSLog] Logged SMS ID {sms_log.id}")
    except Exception as db_ex:
        db.session.rollback()
        current_app.logger.error(f"[SMSLog] DB commit failed: {db_ex}", exc_info=True)

    # Construct TwiML XML response
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{escape(reply)}</Message>
</Response>"""

    return Response(xml_response, mimetype="application/xml")

