from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from db.base import Base


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    connection_id = Column(String, nullable=True)
    shop_name = Column(String, nullable=True)
    name = Column(String, nullable=True)
    tiktok_shop_id = Column(String, nullable=True)
    shop_code = Column(String, nullable=True)
    region = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    raw_payload = Column(Text, nullable=True)

    user = relationship("User", back_populates="shops")
    products = relationship("Product", back_populates="shop", cascade="all, delete-orphan")
    creatives = relationship("Creative", back_populates="shop", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="shop", cascade="all, delete-orphan")
    briefs = relationship("Brief", back_populates="shop", cascade="all, delete-orphan")
    sync_jobs = relationship("SyncJob", back_populates="shop", cascade="all, delete-orphan")
