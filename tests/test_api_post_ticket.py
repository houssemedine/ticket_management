from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_post_ticket_creates_and_returns_ticket() -> None:
    # Crée
    r = client.post("/tickets/", json={"title": "Bug A", "description": "qlq chose qui va pas"})
    assert r.status_code == 201
    data = r.json()
    assert data["title"] == "Bug A"
    assert data["description"] == "qlq chose qui va pas"
    assert data["status"] == "open"
    assert isinstance(data["id"], int)
    assert "created_at" in data

    # Vérifie qu'il apparaît dans la liste
    r2 = client.get("/tickets/")
    assert r2.status_code == 200
    all_items = r2.json()
    assert any(t["id"] == data["id"] for t in all_items)
