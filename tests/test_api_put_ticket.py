from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_put_updates_title_and_description() -> None:
    # crée
    r = client.post("/tickets/", json={"title": "Ancien", "description": "ancien desc"})
    assert r.status_code == 201
    tid = r.json()["id"]

    # update
    r2 = client.put(f"/tickets/{tid}", json={"title": "Nouveau", "description": "nouveau desc"})
    assert r2.status_code == 200
    data = r2.json()
    assert data["id"] == tid
    assert data["title"] == "Nouveau"
    assert data["description"] == "nouveau desc"
    # status ne change pas
    assert data["status"] == "open"

def test_put_returns_404_if_not_found() -> None:
    r = client.put("/tickets/999999", json={"title": "X", "description": "Y"})
    assert r.status_code == 404
    assert r.json()["detail"] == "Ticket not found"

def test_put_validates_input_422() -> None:
    # crée
    r = client.post("/tickets/", json={"title": "A", "description": "B"})
    tid = r.json()["id"]

    # tente un payload invalide (title vide)
    r2 = client.put(f"/tickets/{tid}", json={"title": "", "description": "ok"})
    assert r2.status_code == 422
