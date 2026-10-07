import pytest
from fastapi.testclient import TestClient

import database
from main import app

@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "tasks.db")

    with TestClient(app) as test_client:
        yield test_client

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_version(client):
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json() == {"version": "0.1.0"}

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test Task", "description": "Test task"})

    assert response.status_code == 201

    task = response.json()
    assert task["title"] == "Test Task"
    assert task["description"] == "Test task"
    assert task["completed"] is False

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    assert list_response.json() == [task]

def test_missed_task(client):
    response = client.patch("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_complete_task(client):
    create_response = client.post("/tasks", json={"title": "Complete Task", "description": "Complete Task"})
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(f"/tasks/{task['id']}")
    assert response.status_code == 200



