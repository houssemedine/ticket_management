from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def _make(n: int) -> None:
    for i in range(n):
        client.post("/tickets/", json={"title": f"T{i}", "description": "D"})

def test_pagination_first_page_headers_and_size() -> None:
    _make(25)
    r = client.get("/tickets/?limit=10&offset=0")
    assert r.status_code == 200
    assert r.headers.get("X-Total-Count") == "25"
    data = r.json()
    assert isinstance(data, list) and len(data) == 10
    assert data[0]["title"] == "T0" 
    assert data[-1]["title"] == "T9"

def test_pagination_middle_page() -> None:
    _make(15)
    r = client.get("/tickets/?limit=5&offset=5")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 5

    assert data[0]["title"] == "T5"
    assert data[-1]["title"] == "T9"

def test_pagination_last_partial_page() -> None:
    _make(12)
    r = client.get("/tickets/?limit=10&offset=10")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2

def test_pagination_validation() -> None:
    r = client.get("/tickets/?limit=0")
    assert r.status_code == 422
    r = client.get("/tickets/?limit=101")
    assert r.status_code == 422
    r = client.get("/tickets/?offset=-1")
    assert r.status_code == 422
