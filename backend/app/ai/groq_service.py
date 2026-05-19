import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_ai_reply(user_message: str):

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
You are a professional AI assistant for a car rental and workshop business.

Rules:
- Be concise
- Be professional
- Answer clearly
- If unsure, ask customer to wait for staff
- Never invent pricing
- Never invent payment status
"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        temperature=0.5
    )

    return completion.choices[0].message.content