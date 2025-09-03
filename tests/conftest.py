import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from the_wicker_man.app import app
from the_wicker_man.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        table_registry.metadata.drop_all(engine)
        engine.dispose()
