from app.integrations.whatsapp import send_whatsapp_message
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

OWNER_PHONE = os.getenv("OWNER_PHONE")


async def send_owner_alert(
    customer: str,
    intent: str,
    priority: str,
    message: str
):

    alert_message = f"""
🚨 URGENT CUSTOMER ISSUE

Customer: {customer}

Intent: {intent}

Priority: {priority}

Message:
{message}
"""

    await send_whatsapp_message(
        to=OWNER_PHONE,
        message=alert_message
    )