from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)

    category = Column(String, nullable=False)
    rec_type = Column(String, nullable=True)
    name = Column(String, nullable=False)
    reason = Column(Text, nullable=True)
    confidence = Column(Integer, nullable=True)

    product_name = Column(String, nullable=True)
    evidence = Column(Text, nullable=True)
    action = Column(Text, nullable=True)
    priority = Column(String, nullable=True)
    based_on_creative_ids = Column(Text, nullable=True)

    shop = relationship("Shop", back_populates="recommendations")
