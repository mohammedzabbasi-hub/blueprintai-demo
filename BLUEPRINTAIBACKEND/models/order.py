from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id", ondelete="CASCADE"), nullable=False, index=True)

    tiktok_order_id = Column(String(255), nullable=False, unique=True, index=True)
    buyer_name = Column(String(255), nullable=True)
    order_status = Column(String(100), nullable=True)
    currency = Column(String(16), nullable=True)
    total_amount = Column(Float, nullable=True)
    raw_payload = Column(Text, nullable=True)

    placed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    shop = relationship("Shop")
