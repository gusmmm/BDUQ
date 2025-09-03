from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session as SASession

from the_wicker_man import database
from the_wicker_man.models import table_registry


def test_get_session_yields_session(monkeypatch, tmp_path) -> None:
    # Arrange: create a temporary SQLite engine and patch the module engine

    db_path = tmp_path / 'unit_get_session.db'
    temp_engine = create_engine(
        f'sqlite:///{db_path}', connect_args={"check_same_thread": False}
    )
    table_registry.metadata.create_all(temp_engine)
    monkeypatch.setattr(database, 'engine', temp_engine)

    # Act: get a session from the generator
    gen: Generator = database.get_session()
    sess = next(gen)

    # Assert: type, bind and ability to execute a trivial query
    assert isinstance(sess, SASession)
    # In SQLAlchemy 2.0, binding via `with Session(engine)` sets session.bind
    assert sess.bind is temp_engine
    assert sess.execute(text('SELECT 1')).scalar() == 1

    # Cleanup the generator (triggers context manager exit/close)
    gen.close()

    # Subsequent calls yield a fresh session
    gen2: Generator = database.get_session()
    sess2 = next(gen2)
    try:
        assert isinstance(sess2, SASession)
        assert sess2 is not sess
        assert sess2.bind is temp_engine
        assert sess2.execute(text('SELECT 1')).scalar() == 1
    finally:
        gen2.close()
