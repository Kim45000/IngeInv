"""Pydantic schemas for MaintenanceRecord."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MaintenanceRecordBase(BaseModel):
    machine_id: int
    maintenance_type: str  # preventive | corrective | predictive
    description: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    technician: Optional[str] = None
    cost: Optional[float] = None
    status: str = "scheduled"
    notes: Optional[str] = None


class MaintenanceRecordCreate(MaintenanceRecordBase):
    pass


class MaintenanceRecordUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    technician: Optional[str] = None
    cost: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class MaintenanceRecordOut(MaintenanceRecordBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
