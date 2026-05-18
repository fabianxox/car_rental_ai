from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.db.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    sender = Column(String, nullable=False)

    message = Column(Text, nullable=False)

    direction = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)