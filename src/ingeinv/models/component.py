"""ORM model: Component."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from src.ingeinv.database import Base


class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    name = Column(String(255), nullable=False)
    part_number = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    expected_lifespan_hours = Column(Float, nullable=True)
    current_hours = Column(Float, nullable=False, default=0.0)
    status = Column(String(50), nullable=False, default="ok")
    last_replaced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    machine = relationship("Machine", back_populates="components")
