"""Pydantic schemas for FailurePrediction."""
from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    machine_id: int
    sensor_values: dict[str, float]


class FailurePredictionOut(BaseModel):
    id: int
    machine_id: int
    predicted_failure_type: str
    probability: float
    confidence: Optional[float] = None
    estimated_failure_date: Optional[datetime] = None
    features_snapshot: Optional[str] = None
    recommended_action: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
