# src/ingeinv/models/__init__.py
from .machine import Machine
from .component import Component
from .sensor_reading import SensorReading
from .maintenance_record import MaintenanceRecord
from .failure_prediction import FailurePrediction

__all__ = [
    "Machine",
    "Component",
    "SensorReading",
    "MaintenanceRecord",
    "FailurePrediction",
]
