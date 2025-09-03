import pytest
from fastapi.testclient import TestClient

from the_wicker_man.app import app


@pytest.fixture
def client():
    return TestClient(app)
