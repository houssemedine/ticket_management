from sqlalchemy import inspect
from fastapi.testclient import TestClient
from app.main import app
from app.core.db import engine

def test_startup_creates_tickets_table() -> None:
    with TestClient(app):
        insp = inspect(engine)
        assert "tickets" in insp.get_table_names()
