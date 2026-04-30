"""Router: /maintenance — CRUD + auto-scheduling of maintenance records."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.ingeinv.database import get_db
from src.ingeinv.schemas.maintenance_record import (
    MaintenanceRecordCreate,
    MaintenanceRecordUpdate,
    MaintenanceRecordOut,
)
from src.ingeinv.services.maintenance_service import MaintenanceService

router = APIRouter(prefix="/maintenance", tags=["maintenance"])


@router.post("/", response_model=MaintenanceRecordOut, status_code=status.HTTP_201_CREATED)
def create_record(data: MaintenanceRecordCreate, db: Session = Depends(get_db)):
    return MaintenanceService(db).create(data)


@router.get("/", response_model=List[MaintenanceRecordOut])
def list_records(
    machine_id: Optional[int] = Query(default=None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return MaintenanceService(db).list(machine_id=machine_id, skip=skip, limit=limit)


@router.get("/{record_id}", response_model=MaintenanceRecordOut)
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = MaintenanceService(db).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record


@router.patch("/{record_id}", response_model=MaintenanceRecordOut)
def update_record(record_id: int, data: MaintenanceRecordUpdate, db: Session = Depends(get_db)):
    record = MaintenanceService(db).update(record_id, data)
    if not record:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    if not MaintenanceService(db).delete(record_id):
        raise HTTPException(status_code=404, detail="Registro no encontrado")


@router.post("/schedule/{machine_id}", response_model=MaintenanceRecordOut, status_code=status.HTTP_201_CREATED)
def schedule_preventive(
    machine_id: int,
    days_ahead: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    """Auto-schedule a preventive maintenance order for the given machine."""
    return MaintenanceService(db).schedule_preventive(machine_id, days_ahead=days_ahead)
