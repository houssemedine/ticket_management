from app.core.db import SessionLocal, engine
from app.models.ticket import Base
from app.repositories.tickets import TicketRepository

def test_list_all_returns_empty_initially() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        repo = TicketRepository(db)
        items = repo.list_all()
        assert items == []
    finally:
        db.close()
