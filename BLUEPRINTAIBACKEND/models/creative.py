from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base


class Creative(Base):
    __tablename__ = "creatives"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    product = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    creator = Column(String, nullable=False)

    source_platform = Column(String, nullable=True, default="tiktok")
    video_url = Column(String, nullable=True)
    thumbnail = Column(String, nullable=True)
    insight = Column(Text, nullable=True)
    transcript = Column(Text, nullable=True)
    transcript_summary = Column(Text, nullable=True)

    creator_type = Column(String, nullable=True)
    creator_archetype = Column(String, nullable=True)
    promoter_handle = Column(String, nullable=True)
    humor_style = Column(String, nullable=True)
    delivery_style = Column(String, nullable=True)
    speaking_style = Column(String, nullable=True)
    demo_style = Column(String, nullable=True)
    ad_type = Column(String, nullable=True)
    hook_type = Column(String, nullable=True)
    hook_text = Column(Text, nullable=True)
    cta_style = Column(String, nullable=True)
    primary_subject = Column(String, nullable=True)
    visual_style = Column(String, nullable=True)
    pacing = Column(String, nullable=True)
    text_overlay_style = Column(String, nullable=True)
    winning_reason = Column(Text, nullable=True)
    ai_summary = Column(Text, nullable=True)
    raw_ai_json = Column(Text, nullable=True)

    score = Column(Integer, nullable=True)
    engagement_score = Column(Float, nullable=True)
    conversion_score = Column(Float, nullable=True)

    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    orders = Column(Integer, default=0)

    date = Column(String, nullable=True)

    shop = relationship("Shop", back_populates="creatives")
    product_rel = relationship("Product", back_populates="creatives")
    metrics = relationship("Metric", back_populates="creative", cascade="all, delete-orphan")
    analyses = relationship("VideoAnalysis", back_populates="creative", cascade="all, delete-orphan")
