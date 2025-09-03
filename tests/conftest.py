from contextlib import contextmanager
from datetime import datetime
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from the_wicker_man.app import app
from the_wicker_man.database import get_session
from the_wicker_man.models import table_registry


@pytest.fixture
def engine(tmp_path):
    """Per-test SQLite file-backed engine.
    Using a temporary file avoids SQLite in-memory quirks
    and lets FastAPI/TestClient
    access the same database connection across threads when needed.
    """
    db_path = tmp_path / 'test.db'
    engine = create_engine(
        f'sqlite:///{db_path}',
        connect_args={"check_same_thread": False},
    )
    table_registry.metadata.create_all(engine)
    try:
        yield engine
    finally:
        table_registry.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def session(engine) -> Iterator[Session]:
    """SQLAlchemy session bound to the per-test engine."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session: Session):
    """FastAPI TestClient that uses the same SQLAlchemy
    session via dependency override."""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 9, 13)):

    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time
        if hasattr(target, 'last_modified'):
            target.last_modified = time

    event.listen(model, 'before_insert', fake_time_hook)
    event.listen(model, 'before_update', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)
    event.remove(model, 'before_update', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
