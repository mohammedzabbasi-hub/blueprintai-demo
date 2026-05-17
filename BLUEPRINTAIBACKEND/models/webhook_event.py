from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from db.base import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), nullable=False, default="tiktok_shop")
    event_type = Column(String(255), nullable=True)
    signature = Column(Text, nullable=True)
    payload = Column(Text, nullable=False)

    is_processed = Column(Boolean, nullable=False, default=False)
    processed_at = Column(DateTime, nullable=True)
    processing_error = Column(Text, nullable=True)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
