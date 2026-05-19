import os
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


SMTP_EMAIL = os.getenv("SMTP_EMAIL")

SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

OWNER_EMAIL = os.getenv("OWNER_EMAIL")


def send_urgent_email(
    customer_phone: str,
    intent: str,
    priority: str,
    customer_message: str
):

    subject = f"URGENT CUSTOMER ISSUE - {intent}"

    body = f"""
Urgent customer issue detected.

Customer:
{customer_phone}

Intent:
{intent}

Priority:
{priority}

Message:
{customer_message}
"""

    msg = MIMEText(body)

    msg["Subject"] = subject

    msg["From"] = SMTP_EMAIL

    msg["To"] = OWNER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        smtp.send_message(msg)

    print("URGENT EMAIL SENT")

def send_daily_summary(summary_text):

    subject = "Daily Business Summary"

    msg = MIMEText(summary_text)

    msg["Subject"] = subject

    msg["From"] = SMTP_EMAIL

    msg["To"] = OWNER_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:

        smtp.login(
            SMTP_EMAIL,
            SMTP_PASSWORD
        )

        smtp.send_message(msg)

    print("DAILY SUMMARY SENT")