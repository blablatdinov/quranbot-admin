import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client_factory():
    def _client(app):
        return TestClient(app)

    return _client
