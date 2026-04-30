"""Service layer for Machine CRUD operations."""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.ingeinv.models.machine import Machine
from src.ingeinv.schemas.machine import MachineCreate, MachineUpdate


class MachineService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: MachineCreate) -> Machine:
        machine = Machine(**data.model_dump())
        self.db.add(machine)
        self.db.commit()
        self.db.refresh(machine)
        return machine

    def get(self, machine_id: int) -> Optional[Machine]:
        return self.db.query(Machine).filter(Machine.id == machine_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Machine]:
        return self.db.query(Machine).offset(skip).limit(limit).all()

    def update(self, machine_id: int, data: MachineUpdate) -> Optional[Machine]:
        machine = self.get(machine_id)
        if not machine:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(machine, field, value)
        self.db.commit()
        self.db.refresh(machine)
        return machine

    def delete(self, machine_id: int) -> bool:
        machine = self.get(machine_id)
        if not machine:
            return False
        self.db.delete(machine)
        self.db.commit()
        return True
