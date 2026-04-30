"""Failure prediction service using a simple scikit-learn pipeline.

The model uses sensor telemetry features to estimate the probability and type
of impending failure. In production this model would be trained on historical
failure data; here we ship a rule-based heuristic as a sensible default that
can be replaced by a trained model saved to disk.
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import List, Optional, Tuple

import numpy as np
from sqlalchemy.orm import Session

from src.ingeinv.models.failure_prediction import FailurePrediction
from src.ingeinv.models.sensor_reading import SensorReading


_FAILURE_TYPES = [
    "overheating",
    "vibration_anomaly",
    "pressure_loss",
    "electrical_fault",
    "normal",
]

# Thresholds for the rule-based baseline model
_RULES: dict[str, Tuple[str, float, float]] = {
    # sensor_name → (failure_type, warning_threshold, critical_threshold)
    "temperature": ("overheating", 80.0, 100.0),
    "vibration": ("vibration_anomaly", 5.0, 10.0),
    "pressure": ("pressure_loss", 2.0, 1.0),   # low pressure → fault (inverted)
    "current": ("electrical_fault", 15.0, 20.0),
}


def _heuristic_predict(sensor_values: dict[str, float]) -> Tuple[str, float, str]:
    """Apply rule-based heuristics to produce (failure_type, probability, action).

    Only a reading that exceeds a warning or critical threshold is considered an
    anomaly; below-threshold readings are treated as normal and do not override
    the baseline "normal" failure type.
    """
    best_type = "normal"
    best_prob = 0.05
    best_action = "No se requiere acción inmediata. Continuar monitoreo regular."

    for sensor, value in sensor_values.items():
        sensor_key = sensor.lower()
        for key, (ftype, warn, crit) in _RULES.items():
            if key not in sensor_key:
                continue
            # For pressure the logic is inverted (lower is worse)
            if key == "pressure":
                if value <= crit:
                    prob = 0.90
                elif value <= warn:
                    prob = 0.55
                else:
                    continue  # below threshold → skip
            else:
                if value >= crit:
                    prob = 0.90
                elif value >= warn:
                    prob = 0.55
                else:
                    continue  # below threshold → skip

            if prob > best_prob:
                best_prob = prob
                best_type = ftype
                if prob >= 0.85:
                    best_action = (
                        f"CRÍTICO: Detener máquina y programar mantenimiento correctivo "
                        f"inmediato por {ftype}."
                    )
                else:
                    best_action = (
                        f"ADVERTENCIA: Programar mantenimiento preventivo en los próximos "
                        f"7 días por {ftype}."
                    )

    return best_type, best_prob, best_action


class PredictionService:
    def __init__(self, db: Session):
        self.db = db

    def predict(self, machine_id: int, sensor_values: dict[str, float]) -> FailurePrediction:
        """Run prediction for a machine given current sensor readings and persist the result."""
        failure_type, probability, action = _heuristic_predict(sensor_values)

        estimated_date: Optional[datetime] = None
        if probability >= 0.85:
            estimated_date = datetime.utcnow() + timedelta(days=3)
        elif probability >= 0.50:
            estimated_date = datetime.utcnow() + timedelta(days=14)

        prediction = FailurePrediction(
            machine_id=machine_id,
            predicted_failure_type=failure_type,
            probability=round(probability, 4),
            confidence=round(1 - abs(probability - 0.5) * 0.4, 4),
            estimated_failure_date=estimated_date,
            features_snapshot=json.dumps(sensor_values),
            recommended_action=action,
        )
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def list_for_machine(self, machine_id: int, limit: int = 20) -> List[FailurePrediction]:
        return (
            self.db.query(FailurePrediction)
            .filter(FailurePrediction.machine_id == machine_id)
            .order_by(FailurePrediction.created_at.desc())
            .limit(limit)
            .all()
        )

    def predict_from_stored_readings(self, machine_id: int, last_n: int = 10) -> FailurePrediction:
        """Build a prediction from the most recent stored sensor readings for a machine."""
        rows: List[SensorReading] = (
            self.db.query(SensorReading)
            .filter(SensorReading.machine_id == machine_id)
            .order_by(SensorReading.recorded_at.desc())
            .limit(last_n)
            .all()
        )
        sensor_values: dict[str, float] = {}
        for row in rows:
            # Average duplicate sensor names
            if row.sensor_name in sensor_values:
                sensor_values[row.sensor_name] = (sensor_values[row.sensor_name] + row.value) / 2
            else:
                sensor_values[row.sensor_name] = row.value

        return self.predict(machine_id, sensor_values)
