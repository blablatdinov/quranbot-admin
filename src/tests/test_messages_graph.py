import pytest


def test(client):
    got = client.get('/api/v1/messages/count-graph/')

    assert got.status_code == 200
