import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
def client():
    http_client = TestClient(app)
    http_client.headers = {'Authorization': ''}
    return http_client
