from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_ticket_by_id_returns_200() -> None:
    # crée un ticket
    r = client.post("/tickets/", json={"title": "T1", "description": "Desc"})
    assert r.status_code == 201
    tid = r.json()["id"]

    # récupère par id
    r2 = client.get(f"/tickets/{tid}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["id"] == tid
    assert data["title"] == "T1"
    assert data["status"] == "open"

def test_get_ticket_by_id_returns_404() -> None:
    r = client.get("/tickets/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Ticket not found"
