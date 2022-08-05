from main import app




def override_dependency():
    app.dependency_overrides[]


def test(client):
    got = client.get('/api/v1/messages/count-graph/')

    payload = got.json()

    assert got.status_code == 200
    assert isinstance(payload, list)
    assert list(payload[0].keys()) == ['date', 'messages_count']
