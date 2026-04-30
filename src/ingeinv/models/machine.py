"""ORM model: Machine."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from src.ingeinv.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    model = Column(String(255), nullable=True)
    serial_number = Column(String(255), unique=True, nullable=True)
    location = Column(String(255), nullable=True)
    manufacturer = Column(String(255), nullable=True)
    installation_date = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="operational")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    components = relationship("Component", back_populates="machine", cascade="all, delete-orphan")
    sensor_readings = relationship("SensorReading", back_populates="machine", cascade="all, delete-orphan")
    maintenance_records = relationship("MaintenanceRecord", back_populates="machine", cascade="all, delete-orphan")
    failure_predictions = relationship("FailurePrediction", back_populates="machine", cascade="all, delete-orphan")
