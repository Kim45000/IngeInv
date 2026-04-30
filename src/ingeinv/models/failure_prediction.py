"""ORM model: FailurePrediction — output of the ML prediction engine."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from src.ingeinv.database import Base


class FailurePrediction(Base):
    __tablename__ = "failure_predictions"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    predicted_failure_type = Column(String(255), nullable=False)
    probability = Column(Float, nullable=False)  # 0.0 – 1.0
    confidence = Column(Float, nullable=True)    # model confidence
    estimated_failure_date = Column(DateTime, nullable=True)
    features_snapshot = Column(Text, nullable=True)  # JSON snapshot of input features
    recommended_action = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    machine = relationship("Machine", back_populates="failure_predictions")
