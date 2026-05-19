from fastapi import APIRouter, Request

from app.db.database import SessionLocal
from app.models.message import Message
from app.integrations.whatsapp import send_whatsapp_message
from app.ai.groq_service import generate_ai_reply
from app.ai.intent_classifier import classify_intent
from app.models.conversation import Conversation
from app.services.escalation_service import should_escalate
from app.services.alert_service import send_owner_alert
from app.services.email_service import send_urgent_email

from app.core.logger import logger

router = APIRouter()

VERIFY_TOKEN = "car_rental_secret"


@router.get("/webhook")
async def verify_webhook(request: Request):

    hub_mode = request.query_params.get("hub.mode")
    hub_verify_token = request.query_params.get("hub.verify_token")
    hub_challenge = request.query_params.get("hub.challenge")

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)

    return {"error": "Verification failed"}


@router.post("/webhook")
async def receive_message(request: Request):

    logger.info("WEBHOOK RECEIVED")

    body = await request.json()

    print("INCOMING WEBHOOK:")
    print(body)

    db = SessionLocal()

    try:

        entry = body["entry"][0]

        changes = entry["changes"][0]

        value = changes["value"]

        messages = value.get("messages")

        if messages:

            message_data = messages[0]

            sender = message_data["from"]

            message_type = message_data["type"]

            if message_type == "text":

                text = message_data["text"]["body"]

                logger.info(f"TEXT MESSAGE: {text}")

                # SAVE INCOMING MESSAGE
                incoming = Message(
                    sender=sender,
                    message=text,
                    direction="incoming"
                )

                db.add(incoming)

                db.commit()

                logger.info("INCOMING MESSAGE SAVED")

                # CLASSIFY INTENT
                intent_data = classify_intent(text)

                logger.info(intent_data)

                # SAVE CONVERSATION
                conversation = Conversation(
                    customer_phone=sender,
                    intent=intent_data["intent"],
                    priority=intent_data["priority"]
                )

                db.add(conversation)

                db.commit()

                logger.info("CONVERSATION SAVED")

                # GENERATE AI REPLY
                ai_reply = generate_ai_reply(text)

                logger.info(f"AI REPLY: {ai_reply}")

                # SEND WHATSAPP MESSAGE
                await send_whatsapp_message(
                    to=sender,
                    message=ai_reply
                )

                logger.info("WHATSAPP REPLY SENT")

                # SAVE OUTGOING MESSAGE
                outgoing = Message(
                    sender=sender,
                    message=ai_reply,
                    direction="outgoing"
                )

                db.add(outgoing)

                db.commit()

                logger.info("OUTGOING MESSAGE SAVED")

                # ESCALATION
                is_urgent = should_escalate(
                    intent_data["priority"]
                )

                if is_urgent:

                    logger.warning("URGENT ISSUE DETECTED")

                    send_urgent_email(
                        customer_phone=sender,
                        intent=intent_data["intent"],
                        priority=intent_data["priority"],
                        customer_message=text
                    )

                    logger.warning("URGENT EMAIL SENT")

    except Exception as e:

        logger.error(f"WEBHOOK ERROR: {e}")

    finally:

        db.close()

    return {"status": "received"}


@router.post("/test")
async def test_post():

    logger.info("TEST POST WORKING")

    return {"status": "ok"}