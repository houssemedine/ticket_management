from fastapi.testclient import TestClient
from app.main import app
from app.core.db import SessionLocal
from app.models.ticket import Ticket

def test_list_tickets_initially_empty() -> None:
    with TestClient(app) as client:
        r = client.get("/tickets/")
        assert r.status_code == 200
        assert r.json() == []

def test_list_tickets_returns_inserted_row() -> None:
    db = SessionLocal()
    try:
        t = Ticket(title="First", description="Hello")
        db.add(t)
        db.commit()
        db.refresh(t)
    finally:
        db.close()

    # Vérifie via l'API
    with TestClient(app) as client:
        r = client.get("/tickets/")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list) and len(data) >= 1

        found = next((x for x in data if x["title"] == "First"), None)
        assert found is not None
        assert found["description"] == "Hello"
        assert found["status"] == "open"
        assert isinstance(found["id"], int)
        assert "created_at" in found
