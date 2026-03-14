from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./gpt_model.db"

try:

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    SessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )

except Exception as f:
    print(f"Error: {f}.")

    Base = declarative_base()