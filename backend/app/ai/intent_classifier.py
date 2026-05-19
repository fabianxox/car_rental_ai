from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def classify_intent(message: str):

    prompt = f"""
Classify this customer message.

Possible intents:
- rental_booking
- pricing_question
- payment_issue
- accident_report
- workshop_booking
- complaint
- general_question

Also classify priority:
- low
- normal
- high
- urgent

Return ONLY valid JSON.

Example:
{{
    "intent": "payment_issue",
    "priority": "high"
}}

Message:
{message}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    response = completion.choices[0].message.content

    return json.loads(response)