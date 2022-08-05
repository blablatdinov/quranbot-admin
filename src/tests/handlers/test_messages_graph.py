import pytest


def test(client):
    got = client.get('/api/v1/messages/count-graph/')

    payload = got.json()

    assert got.status_code == 200
    assert isinstance(payload, list)
    assert list(payload[0].keys()) == ['date', 'messages_count']
