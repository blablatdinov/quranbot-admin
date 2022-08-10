import pytest


@pytest.fixture()
def file():
    return b''


def test(client, file):
    got = client.post('/api/v1/files/', files={'file': file})

    assert got.status_code == 201
