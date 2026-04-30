"""Tests for /maintenance endpoints."""
from fastapi.testclient import TestClient


def _create_machine(client: TestClient, name: str = "Test Machine") -> dict:
    return client.post("/machines/", json={"name": name}).json()


def test_create_maintenance_record(client: TestClient):
    machine = _create_machine(client)
    resp = client.post(
        "/maintenance/",
        json={
            "machine_id": machine["id"],
            "maintenance_type": "preventive",
            "description": "Cambio de filtros",
            "status": "scheduled",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["maintenance_type"] == "preventive"
    assert data["status"] == "scheduled"


def test_list_maintenance_records(client: TestClient):
    machine = _create_machine(client)
    mid = machine["id"]
    client.post("/maintenance/", json={"machine_id": mid, "maintenance_type": "corrective"})
    client.post("/maintenance/", json={"machine_id": mid, "maintenance_type": "preventive"})
    resp = client.get(f"/maintenance/?machine_id={mid}")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_maintenance_record(client: TestClient):
    machine = _create_machine(client)
    record = client.post(
        "/maintenance/",
        json={"machine_id": machine["id"], "maintenance_type": "corrective"},
    ).json()
    resp = client.patch(f"/maintenance/{record['id']}", json={"status": "done"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "done"


def test_delete_maintenance_record(client: TestClient):
    machine = _create_machine(client)
    record = client.post(
        "/maintenance/",
        json={"machine_id": machine["id"], "maintenance_type": "predictive"},
    ).json()
    del_resp = client.delete(f"/maintenance/{record['id']}")
    assert del_resp.status_code == 204
    get_resp = client.get(f"/maintenance/{record['id']}")
    assert get_resp.status_code == 404


def test_schedule_preventive_maintenance(client: TestClient):
    machine = _create_machine(client)
    resp = client.post(f"/maintenance/schedule/{machine['id']}?days_ahead=14")
    assert resp.status_code == 201
    data = resp.json()
    assert data["maintenance_type"] == "preventive"
    assert data["status"] == "scheduled"
    assert data["machine_id"] == machine["id"]
