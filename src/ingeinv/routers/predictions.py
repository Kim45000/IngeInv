"""Router: /predictions — Failure prediction endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.ingeinv.database import get_db
from src.ingeinv.models.machine import Machine
from src.ingeinv.models.sensor_reading import SensorReading
from src.ingeinv.schemas.sensor_reading import SensorReadingCreate, SensorReadingOut
from src.ingeinv.schemas.failure_prediction import FailurePredictionOut, PredictionRequest
from src.ingeinv.services.prediction_service import PredictionService

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/", response_model=FailurePredictionOut, status_code=status.HTTP_201_CREATED)
def run_prediction(data: PredictionRequest, db: Session = Depends(get_db)):
    """Run failure prediction for a machine given a snapshot of sensor values."""
    machine = db.query(Machine).filter(Machine.id == data.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return PredictionService(db).predict(data.machine_id, data.sensor_values)


@router.get("/{machine_id}", response_model=List[FailurePredictionOut])
def list_predictions(machine_id: int, limit: int = 20, db: Session = Depends(get_db)):
    """List the most recent failure predictions for a machine."""
    return PredictionService(db).list_for_machine(machine_id, limit=limit)


@router.post("/{machine_id}/from-stored-readings", response_model=FailurePredictionOut, status_code=status.HTTP_201_CREATED)
def predict_from_stored(machine_id: int, last_n: int = 10, db: Session = Depends(get_db)):
    """Predict failure using the most recently stored sensor readings for a machine."""
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    return PredictionService(db).predict_from_stored_readings(machine_id, last_n=last_n)


# ── Sensor readings ingestion ─────────────────────────────────────────────────

@router.post("/readings/", response_model=SensorReadingOut, status_code=status.HTTP_201_CREATED)
def ingest_reading(data: SensorReadingCreate, db: Session = Depends(get_db)):
    """Ingest a single sensor reading for a machine."""
    machine = db.query(Machine).filter(Machine.id == data.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Máquina no encontrada")
    row = SensorReading(**data.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
