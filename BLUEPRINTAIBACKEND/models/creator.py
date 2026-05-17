from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

try:
    from db.database import Base
except ModuleNotFoundError:
    from app.db.database import Base


class Creator(Base):
    __tablename__ = "creators"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, nullable=True, index=True)
    brand_id = Column(Integer, nullable=True, index=True)

    name = Column(String, nullable=False)
    tiktok_handle = Column(String, nullable=False, index=True)
    profile_image = Column(String, nullable=True)

    follower_count = Column(Integer, default=0)
    category = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    total_videos = Column(Integer, default=0)
    total_views = Column(Integer, default=0)
    total_likes = Column(Integer, default=0)
    total_comments = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    total_conversions = Column(Integer, default=0)
    total_revenue = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
