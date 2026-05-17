from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    creative_id = Column(Integer, ForeignKey("creatives.id"), nullable=False, index=True)

    views = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    orders = Column(Integer, default=0)

    ctr = Column(Float, nullable=True)
    cvr = Column(Float, nullable=True)
    roas = Column(Float, nullable=True)

    creative = relationship("Creative", back_populates="metrics")
