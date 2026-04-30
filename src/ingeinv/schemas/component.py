"""Pydantic schemas for Component."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ComponentBase(BaseModel):
    machine_id: int
    name: str
    part_number: Optional[str] = None
    description: Optional[str] = None
    expected_lifespan_hours: Optional[float] = None
    current_hours: float = 0.0
    status: str = "ok"
    last_replaced_at: Optional[datetime] = None


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    name: Optional[str] = None
    part_number: Optional[str] = None
    description: Optional[str] = None
    expected_lifespan_hours: Optional[float] = None
    current_hours: Optional[float] = None
    status: Optional[str] = None
    last_replaced_at: Optional[datetime] = None


class ComponentOut(ComponentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
