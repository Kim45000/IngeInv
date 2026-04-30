"""Service layer for Maintenance planning and CRUD operations."""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.orm import Session
from src.ingeinv.models.maintenance_record import MaintenanceRecord
from src.ingeinv.schemas.maintenance_record import MaintenanceRecordCreate, MaintenanceRecordUpdate


class MaintenanceService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: MaintenanceRecordCreate) -> MaintenanceRecord:
        record = MaintenanceRecord(**data.model_dump())
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get(self, record_id: int) -> Optional[MaintenanceRecord]:
        return self.db.query(MaintenanceRecord).filter(MaintenanceRecord.id == record_id).first()

    def list(self, machine_id: Optional[int] = None, skip: int = 0, limit: int = 100) -> List[MaintenanceRecord]:
        query = self.db.query(MaintenanceRecord)
        if machine_id is not None:
            query = query.filter(MaintenanceRecord.machine_id == machine_id)
        return query.offset(skip).limit(limit).all()

    def update(self, record_id: int, data: MaintenanceRecordUpdate) -> Optional[MaintenanceRecord]:
        record = self.get(record_id)
        if not record:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(record, field, value)
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record_id: int) -> bool:
        record = self.get(record_id)
        if not record:
            return False
        self.db.delete(record)
        self.db.commit()
        return True

    def schedule_preventive(self, machine_id: int, days_ahead: int = 30) -> MaintenanceRecord:
        """Automatically schedule a preventive maintenance order for a machine."""
        data = MaintenanceRecordCreate(
            machine_id=machine_id,
            maintenance_type="preventive",
            description="Mantenimiento preventivo programado automáticamente",
            scheduled_date=datetime.utcnow() + timedelta(days=days_ahead),
            status="scheduled",
        )
        return self.create(data)
