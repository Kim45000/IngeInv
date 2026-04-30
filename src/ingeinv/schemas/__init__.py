# src/ingeinv/schemas/__init__.py
from .machine import MachineCreate, MachineUpdate, MachineOut
from .component import ComponentCreate, ComponentUpdate, ComponentOut
from .sensor_reading import SensorReadingCreate, SensorReadingOut
from .maintenance_record import MaintenanceRecordCreate, MaintenanceRecordUpdate, MaintenanceRecordOut
from .failure_prediction import FailurePredictionOut, PredictionRequest

__all__ = [
    "MachineCreate", "MachineUpdate", "MachineOut",
    "ComponentCreate", "ComponentUpdate", "ComponentOut",
    "SensorReadingCreate", "SensorReadingOut",
    "MaintenanceRecordCreate", "MaintenanceRecordUpdate", "MaintenanceRecordOut",
    "FailurePredictionOut", "PredictionRequest",
]
