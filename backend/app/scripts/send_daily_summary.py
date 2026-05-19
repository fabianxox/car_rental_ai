from app.db.database import SessionLocal
from app.models.conversation import Conversation

from datetime import datetime, timedelta


def get_todays_conversations():

    db = SessionLocal()

    today_start = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    today_end = today_start + timedelta(days=1)

    conversations = db.query(Conversation).filter(
        Conversation.created_at >= today_start,
        Conversation.created_at < today_end
    ).all()

    db.close()

    return conversations