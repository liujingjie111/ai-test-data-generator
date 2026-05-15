"""Generation history database model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

from app.database import Base


class GenerationHistory(Base):
    __tablename__ = "generation_history"

    id = Column(Integer, primary_key=True, index=True)
    generator_type = Column(String(50), nullable=False, index=True)
    count = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="completed", index=True)
    params = Column(Text, nullable=True)
    result_data = Column(Text, nullable=True)
    error_msg = Column(Text, nullable=True)
    client_ip = Column(String(45), nullable=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)