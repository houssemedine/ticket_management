import pytest
from app.core.db import engine
from app.models.ticket import Base

@pytest.fixture(autouse=True)
def _reset_db():
    # Schéma propre avant chaque test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # (optionnel) cleanup après test
    Base.metadata.drop_all(bind=engine)
