from app.db.database import SessionLocal
from app.models.conversation import Conversation

from datetime import datetime


def get_todays_conversations():

    db = SessionLocal()

    conversations = db.query(Conversation).all()

    db.close()

    return conversations