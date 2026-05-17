from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base


class VideoAnalysis(Base):
    __tablename__ = "video_analyses"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False, index=True)
    creative_id = Column(Integer, ForeignKey("creatives.id"), nullable=True, index=True)

    source_url = Column(String, nullable=True)
    source_platform = Column(String, nullable=False, default="tiktok")
    brand_name = Column(String, nullable=True)
    product_name = Column(String, nullable=True)

    transcript = Column(Text, nullable=True)
    transcript_summary = Column(Text, nullable=True)
    frames_json = Column(Text, nullable=True)

    hook_type = Column(String, nullable=True)
    hook_text = Column(Text, nullable=True)
    humor_style = Column(String, nullable=True)
    delivery_style = Column(String, nullable=True)
    creator_style = Column(String, nullable=True)
    promoter_type = Column(String, nullable=True)
    subject_focus = Column(String, nullable=True)
    pacing = Column(String, nullable=True)
    cta_style = Column(String, nullable=True)

    performance_hypothesis = Column(Text, nullable=True)
    strengths = Column(Text, nullable=True)
    weaknesses = Column(Text, nullable=True)
    structured_output_json = Column(Text, nullable=True)

    creative = relationship("Creative", back_populates="analyses")
