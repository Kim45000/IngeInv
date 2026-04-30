"""Tests for the /machines endpoints."""
import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_machine(client: TestClient):
    resp = client.post("/machines/", json={"name": "Compresor A", "location": "Planta 1"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Compresor A"
    assert data["location"] == "Planta 1"
    assert data["status"] == "operational"
    assert "id" in data


def test_list_machines(client: TestClient):
    client.post("/machines/", json={"name": "Máquina 1"})
    client.post("/machines/", json={"name": "Máquina 2"})
    resp = client.get("/machines/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_machine(client: TestClient):
    created = client.post("/machines/", json={"name": "Torno CNC"}).json()
    resp = client.get(f"/machines/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Torno CNC"


def test_get_machine_not_found(client: TestClient):
    resp = client.get("/machines/9999")
    assert resp.status_code == 404


def test_update_machine(client: TestClient):
    created = client.post("/machines/", json={"name": "Prensa"}).json()
    resp = client.patch(f"/machines/{created['id']}", json={"status": "maintenance"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "maintenance"


def test_delete_machine(client: TestClient):
    created = client.post("/machines/", json={"name": "Bomba hidráulica"}).json()
    del_resp = client.delete(f"/machines/{created['id']}")
    assert del_resp.status_code == 204
    get_resp = client.get(f"/machines/{created['id']}")
    assert get_resp.status_code == 404


def test_add_and_list_components(client: TestClient):
    machine = client.post("/machines/", json={"name": "Motor eléctrico"}).json()
    mid = machine["id"]
    comp_resp = client.post(
        f"/machines/{mid}/components",
        json={
            "machine_id": mid,
            "name": "Rodamiento SKF",
            "expected_lifespan_hours": 5000.0,
            "current_hours": 1200.0,
        },
    )
    assert comp_resp.status_code == 201
    assert comp_resp.json()["name"] == "Rodamiento SKF"

    list_resp = client.get(f"/machines/{mid}/components")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1


def test_update_component(client: TestClient):
    machine = client.post("/machines/", json={"name": "Fresa"}).json()
    mid = machine["id"]
    comp = client.post(
        f"/machines/{mid}/components",
        json={"machine_id": mid, "name": "Eje principal"},
    ).json()
    cid = comp["id"]
    resp = client.patch(f"/machines/{mid}/components/{cid}", json={"status": "worn"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "worn"
