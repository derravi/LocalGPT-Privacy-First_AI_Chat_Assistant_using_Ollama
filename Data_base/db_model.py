from sqlalchemy import Column,Integer,Text, DateTime
from datetime import datetime
from .db_engine import Base,SessionLocal

class gpt_model(Base):
    __tablename__ = "gpt_prompts"

    id = Column(Integer,primary_key=True,index=True)
    original_text = Column(Text)
    answer_text = Column(Text)
    time_stemp = Column(datetime,default=datetime.utcnow)
