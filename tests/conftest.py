from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
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


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 9, 13)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'last_modified'):
            target.last_modified = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
