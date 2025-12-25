import os
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

from dotenv import load_dotenv

load_dotenv()

NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")

if not NEON_DATABASE_URL:
    raise ValueError("NEON_DATABASE_URL environment variable not set.")

engine = create_engine(NEON_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    history = Column(JSONB, nullable=False, default=lambda: [])

class QueryLog(Base):
    __tablename__ = "query_logs"
    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), nullable=False) # Foreign Key is not explicitly enforced here but assumed
    query = Column(Text, nullable=False)
    retrieved_chunks = Column(JSONB, nullable=False, default=lambda: [])
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def create_db_tables():
    Base.metadata.create_all(bind=engine)
    print("Database tables created/checked.")

# Example of how to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    create_db_tables()
