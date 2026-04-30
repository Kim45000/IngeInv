"""Tests for /predictions endpoints and the prediction logic."""
import pytest
from fastapi.testclient import TestClient
from src.ingeinv.services.prediction_service import _heuristic_predict


def _create_machine(client: TestClient, name: str = "Test Machine") -> dict:
    return client.post("/machines/", json={"name": name}).json()


# ── Unit tests for heuristic engine ──────────────────────────────────────────

def test_heuristic_normal():
    ftype, prob, action = _heuristic_predict({"temperature": 40.0, "vibration": 1.0})
    assert ftype == "normal"
    assert prob < 0.5


def test_heuristic_overheating_warning():
    ftype, prob, action = _heuristic_predict({"temperature": 85.0})
    assert ftype == "overheating"
    assert 0.5 <= prob < 0.9


def test_heuristic_overheating_critical():
    ftype, prob, action = _heuristic_predict({"temperature": 110.0})
    assert ftype == "overheating"
    assert prob >= 0.85


def test_heuristic_pressure_loss_critical():
    ftype, prob, action = _heuristic_predict({"pressure": 0.5})
    assert ftype == "pressure_loss"
    assert prob >= 0.85


def test_heuristic_picks_worst_sensor():
    # vibration is at critical, temperature is at warning level → vibration_anomaly wins
    ftype, prob, action = _heuristic_predict({"temperature": 85.0, "vibration": 12.0})
    assert ftype == "vibration_anomaly"
    assert prob >= 0.85


# ── Integration tests via HTTP ────────────────────────────────────────────────

def test_ingest_sensor_reading(client: TestClient):
    machine = _create_machine(client)
    resp = client.post(
        "/predictions/readings/",
        json={"machine_id": machine["id"], "sensor_name": "temperature", "value": 75.0, "unit": "°C"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["sensor_name"] == "temperature"
    assert data["value"] == 75.0


def test_run_prediction_normal(client: TestClient):
    machine = _create_machine(client)
    resp = client.post(
        "/predictions/",
        json={"machine_id": machine["id"], "sensor_values": {"temperature": 50.0, "vibration": 2.0}},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["predicted_failure_type"] == "normal"
    assert data["probability"] < 0.5


def test_run_prediction_overheating(client: TestClient):
    machine = _create_machine(client)
    resp = client.post(
        "/predictions/",
        json={"machine_id": machine["id"], "sensor_values": {"temperature": 105.0}},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["predicted_failure_type"] == "overheating"
    assert data["probability"] >= 0.85
    assert data["estimated_failure_date"] is not None


def test_list_predictions(client: TestClient):
    machine = _create_machine(client)
    mid = machine["id"]
    client.post("/predictions/", json={"machine_id": mid, "sensor_values": {"temperature": 50.0}})
    client.post("/predictions/", json={"machine_id": mid, "sensor_values": {"vibration": 8.0}})
    resp = client.get(f"/predictions/{mid}")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_predict_from_stored_readings(client: TestClient):
    machine = _create_machine(client)
    mid = machine["id"]
    # Ingest some readings
    for _ in range(3):
        client.post("/predictions/readings/", json={"machine_id": mid, "sensor_name": "temperature", "value": 110.0})

    resp = client.post(f"/predictions/{mid}/from-stored-readings")
    assert resp.status_code == 201
    data = resp.json()
    assert data["predicted_failure_type"] == "overheating"


def test_prediction_machine_not_found(client: TestClient):
    resp = client.post(
        "/predictions/",
        json={"machine_id": 9999, "sensor_values": {"temperature": 50.0}},
    )
    assert resp.status_code == 404
