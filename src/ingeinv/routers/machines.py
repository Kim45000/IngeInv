"""Router: /machines — CRUD for machines and their components."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.ingeinv.database import get_db
from src.ingeinv.schemas.machine import MachineCreate, MachineUpdate, MachineOut
from src.ingeinv.schemas.component import ComponentCreate, ComponentUpdate, ComponentOut
from src.ingeinv.services.machine_service import MachineService
from src.ingeinv.models.component import Component

router = APIRouter(prefix="/machines", tags=["machines"])


# ── Machines ─────────────────────────────────────────────────────────────────

@router.post("/", response_model=MachineOut, status_code=status.HTTP_201_CREATED)
def create_machine(data: MachineCreate, db: Session = Depends(get_db)):
    return MachineService(db).create(data)


@router.get("/", response_model=List[MachineOut])
def list_machines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return MachineService(db).list(skip=skip, limit=limit)


@router.get("/{machine_id}", response_model=MachineOut)
def get_machine(machine_id: int, db: Session = Depends(get_db)):
    machine = MachineService(db).get(machine_id)
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return machine


@router.patch("/{machine_id}", response_model=MachineOut)
def update_machine(machine_id: int, data: MachineUpdate, db: Session = Depends(get_db)):
    machine = MachineService(db).update(machine_id, data)
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return machine


@router.delete("/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    if not MachineService(db).delete(machine_id):
        raise HTTPException(status_code=404, detail="Máquina no encontrada")


# ── Components ────────────────────────────────────────────────────────────────

@router.post("/{machine_id}/components", response_model=ComponentOut, status_code=status.HTTP_201_CREATED)
def add_component(machine_id: int, data: ComponentCreate, db: Session = Depends(get_db)):
    if not MachineService(db).get(machine_id):
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    data_dict = data.model_dump()
    data_dict["machine_id"] = machine_id
    component = Component(**data_dict)
    db.add(component)
    db.commit()
    db.refresh(component)
    return component


@router.get("/{machine_id}/components", response_model=List[ComponentOut])
def list_components(machine_id: int, db: Session = Depends(get_db)):
    return db.query(Component).filter(Component.machine_id == machine_id).all()


@router.patch("/{machine_id}/components/{component_id}", response_model=ComponentOut)
def update_component(machine_id: int, component_id: int, data: ComponentUpdate, db: Session = Depends(get_db)):
    component = db.query(Component).filter(
        Component.id == component_id, Component.machine_id == machine_id
    ).first()
    if not component:
        raise HTTPException(status_code=404, detail="Componente no encontrado")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(component, field, value)
    db.commit()
    db.refresh(component)
    return component
