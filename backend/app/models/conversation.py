from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.db.database import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)

    customer_phone = Column(String, nullable=False)

    intent = Column(String, nullable=True)

    priority = Column(String, default="normal")

    status = Column(String, default="open")

    created_at = Column(DateTime, default=datetime.utcnow)