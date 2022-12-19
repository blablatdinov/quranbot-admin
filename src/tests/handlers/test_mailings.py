import pytest


@pytest.mark.usefixtures('override_auth_dep', 'override_queue_dep')
def test_get_mailings(client):
    got = client.get('/api/v1/mailings')

    assert got.status_code == 200


@pytest.mark.usefixtures('override_auth_dep', 'override_queue_dep')
def test_delete_mailing_from_telegram(client):
    got = client.delete('/api/v1/mailings/23')

    assert got.status_code == 201, got.json()


@pytest.mark.usefixtures('override_auth_dep', 'override_queue_dep')
def test_create_mailing(client):
    got = client.post('/api/v1/mailings/', json={
        'text': 'some text',
    })

    assert got.status_code == 201
