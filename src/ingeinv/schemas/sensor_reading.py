"""Pydantic schemas for SensorReading."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class SensorReadingCreate(BaseModel):
    machine_id: int
    sensor_name: str
    value: float
    unit: Optional[str] = None
    recorded_at: Optional[datetime] = None


class SensorReadingOut(SensorReadingCreate):
    id: int
    recorded_at: datetime

    model_config = {"from_attributes": True}
