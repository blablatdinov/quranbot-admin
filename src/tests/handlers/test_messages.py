import pytest


@pytest.mark.slow
def test_get_list(client):
    got = client.get('/api/v1/messages')

    assert got.status_code == 200
    assert got.json() == {
        'count': 2,
        'next': '/api/v1/messages/?page=2',
        'prev': '/api/v1/messages/?page=0',
        'results': [
            {
                'ayat_id': 1,
                'message_id': 1,
                'message_source': 'from 23343',
                'sending_date': '1000-01-01T00:00:00',
                'text': 'Hello...',
            },
            {
                'ayat_id': 2,
                'message_id': 10,
                'message_source': 'Mailing (45)',
                'sending_date': '1000-01-01T00:00:00',
                'text': 'Bye...',
            },
        ],
    }


@pytest.mark.slow
def test_get_message(client):
    got = client.get('/api/v1/messages/34')

    assert got.status_code == 200
    assert got.json() == {
        'ayat_id': 34,
        'message_id': 1,
        'message_source': 'from 23343',
        'sending_date': '1000-01-01T00:00:00',
        'text': 'Hello...',
    }


@pytest.mark.slow
def test_delete_message_from_telegram(client):
    got = client.delete('/api/v1/messages/34/delete-from-chat')

    assert got.status_code == 204
