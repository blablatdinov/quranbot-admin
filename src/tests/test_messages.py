from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test():
    got = client.get('/api/v1/messages')

    assert got.status_code == 200
