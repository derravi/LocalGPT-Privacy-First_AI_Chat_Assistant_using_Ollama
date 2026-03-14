from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from datetime import datetime
from Data_base.db_engine import Base

try:
    class chat_session(Base):

        __tablename__ = "chat_session"

        id = Column(Integer, primary_key=True, index=True)
        title = Column(Text)

except Exception as g:
    print(f"Error: {g}.")

try:
    class gpt_model(Base):

        __tablename__ = "gpt_model"

        id = Column(Integer, primary_key=True, index=True)
        session_id = Column(Integer, ForeignKey("chat_session.id"))
        original_text = Column(Text)
        answer_text = Column(Text)
        time_stemp = Column(DateTime, default=datetime.utcnow)

except Exception as g1:
    print(f"Error: {g1}.")