from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from .db_engine import Base


class chat_session(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class gpt_model(Base):
    __tablename__ = "gpt_prompts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    original_text = Column(Text)
    answer_text = Column(Text)
    time_stemp = Column(DateTime, default=datetime.utcnow)