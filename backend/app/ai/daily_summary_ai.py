import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_daily_summary(conversations):

    formatted_data = ""

    for convo in conversations:

        formatted_data += f"""
Customer: {convo.customer_phone}
Intent: {convo.intent}
Priority: {convo.priority}
"""

    prompt = f"""
You are an AI business assistant.

Generate a concise daily business summary.

Focus on:
- customer enquiries
- bookings
- complaints
- urgent issues
- payment discussions
- workshop jobs

Data:
{formatted_data}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content