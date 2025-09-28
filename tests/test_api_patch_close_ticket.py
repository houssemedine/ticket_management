from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_patch_close_ticket_sets_status_closed() -> None:
    # crée
    r = client.post("/tickets/", json={"title": "To close", "description": "Desc"})
    tid = r.json()["id"]

    # ferme
    r2 = client.patch(f"/tickets/{tid}/close")
    assert r2.status_code == 200
    data = r2.json()
    assert data["id"] == tid
    assert data["status"] == "closed"

def test_patch_close_ticket_returns_400_if_already_closed() -> None:
    # crée
    r = client.post("/tickets/", json={"title": "X", "description": "Y"})
    tid = r.json()["id"]

    # 1er close → OK
    r1 = client.patch(f"/tickets/{tid}/close")
    assert r1.status_code == 200
    assert r1.json()["status"] == "closed"

    # 2e close → 400 "already closed"
    r2 = client.patch(f"/tickets/{tid}/close")
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Ticket is already closed"

def test_patch_close_ticket_404_if_not_found() -> None:
    r = client.patch("/tickets/999999/close")
    assert r.status_code == 404
    assert r.json()["detail"] == "Ticket not found"
