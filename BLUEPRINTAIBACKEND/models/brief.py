from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base


class Brief(Base):
    __tablename__ = "briefs"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)

    product = Column(String, nullable=False)
    brief_title = Column(String, nullable=True)
    hook = Column(String, nullable=False)
    creator_type = Column(String, nullable=False)
    tone = Column(String, nullable=True)
    structure = Column(Text, nullable=True)
    cta = Column(String, nullable=True)
    reasoning = Column(Text, nullable=True)

    target_audience = Column(Text, nullable=True)
    primary_angle = Column(Text, nullable=True)
    secondary_angle = Column(Text, nullable=True)
    script = Column(Text, nullable=True)
    shot_list = Column(Text, nullable=True)
    dos = Column(Text, nullable=True)
    donts = Column(Text, nullable=True)
    references = Column(Text, nullable=True)
    raw_ai_json = Column(Text, nullable=True)

    shop = relationship("Shop", back_populates="briefs")
    product_rel = relationship("Product", back_populates="briefs")
