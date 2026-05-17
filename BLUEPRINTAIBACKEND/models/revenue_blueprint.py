from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.base import Base


class RevenueBlueprint(Base):
    __tablename__ = "revenue_blueprints"

    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"), nullable=False, index=True)

    title = Column(String(255), default="AI Growth Blueprint")
    main_goal = Column(String(255), nullable=True)
    diagnosis = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    estimated_impact = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    steps = relationship(
        "RevenueBlueprintStep",
        back_populates="blueprint",
        cascade="all, delete-orphan",
    )


class RevenueBlueprintStep(Base):
    __tablename__ = "revenue_blueprint_steps"

    id = Column(Integer, primary_key=True, index=True)
    blueprint_id = Column(Integer, ForeignKey("revenue_blueprints.id"), nullable=False, index=True)

    step_number = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    action = Column(Text, nullable=False)

    priority = Column(String(50), default="Medium")
    related_feature = Column(String(100), nullable=True)
    expected_result = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)

    blueprint = relationship("RevenueBlueprint", back_populates="steps")
