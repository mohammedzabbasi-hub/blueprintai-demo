from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base


class ShopConnection(Base):
    __tablename__ = "shop_connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    platform = Column(String, nullable=False, default="tiktok")
    access_token = Column(Text, nullable=True)
    refresh_token = Column(Text, nullable=True)
    shop_cipher = Column(String, nullable=True)
    shop_id_on_platform = Column(String, nullable=True)
    access_token_expires_at = Column(DateTime, nullable=True)
    refresh_token_expires_at = Column(DateTime, nullable=True)
    is_connected = Column(Boolean, nullable=False, default=True)
    raw_payload = Column(Text, nullable=True)

    user = relationship("User", back_populates="shop_connections")
