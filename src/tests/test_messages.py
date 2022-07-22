from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_list():
    got = client.get('/api/v1/messages')

    assert got.status_code == 200
    assert got.json() == {
        'count': 2,
        'next': '/api/v1/messages/?page=2',
        'prev': '/api/v1/messages/?page=0',
        'results': [
            {
                'id': 1,
                'message_id': 1,
                'message_source': 'from 23343',
                'sending_date': '1000-01-01T00:00:00',
                'text': 'Hello...',
            },
            {
                'id': 2,
                'message_id': 10,
                'message_source': 'Mailing (45)',
                'sending_date': '1000-01-01T00:00:00',
                'text': 'Bye...',
            },
        ],
    }


def test_get_message():
    got = client.get('/api/v1/messages/34')

    assert got.status_code == 200
    assert got.json() == {
        'id': 34,
        'message_id': 1,
        'message_source': 'from 23343',
        'sending_date': '1000-01-01T00:00:00',
        'text': 'Hello...',
    }


def test_delete_message_from_telegram():
    got = client.delete('/api/v1/messages/34/delete-from-chat')

    assert got.status_code == 204
