import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture()
def client_factory():
    def _client(app):
        return TestClient(app)

    return _client


@pytest.fixture()
def client():
    return TestClient(app)
