from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False)

    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=True)
    price = Column(Float, nullable=True)

    shop = relationship("Shop", back_populates="products")
    creatives = relationship("Creative", back_populates="product_rel")
    briefs = relationship("Brief", back_populates="product_rel")
