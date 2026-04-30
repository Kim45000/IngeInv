"""Pydantic schemas for Machine."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MachineBase(BaseModel):
    name: str
    model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    manufacturer: Optional[str] = None
    installation_date: Optional[datetime] = None
    status: str = "operational"
    notes: Optional[str] = None


class MachineCreate(MachineBase):
    pass


class MachineUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    location: Optional[str] = None
    manufacturer: Optional[str] = None
    installation_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class MachineOut(MachineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
