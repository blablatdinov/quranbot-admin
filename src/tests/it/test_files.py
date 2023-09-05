import json
from pathlib import Path

import pika

from settings import settings


def test(pgsql, client):
    got = client.get('/api/v1/files/')

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert len(got.json()['results']) == 50
    assert list(
        got.json()['results'][0].keys(),
    ) == [
        'id',
        'link',
        'telegram_file_id',
        'name',
    ]


def test_create_file(pgsql, client, freezer):
    freezer.move_to('2023-09-05')
    got = client.post('/api/v1/files/', files={
        'file': ('empty.mp3', Path('src/tests/fixtures/empty.mp3').read_bytes()),
    })
    published_event = json.loads(
        pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                port=5672,
                credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS),
            ),
        )
        .channel()
        .basic_get(queue='my_queue', auto_ack=True)[2]
        .decode('utf-8'),
    )

    assert got.status_code == 201, got.content
    assert {
        key: value
        for key, value in published_event.items()
        if key not in ('event_id', 'data')
    } == {
        'event_name': 'File.SendTriggered',
        'event_time': '1693872000',
        'event_version': 1,
        'producer': 'quranbot-admin',
    }
    assert {
        key: value
        for key, value in published_event['data'].items()
        if key != 'file_id'
    } == {
        'path': '/Users/almazilaletdinov/code/quranbot/admin/media/empty.mp3',
        'source': 'disk',
    }
    assert Path(published_event['data']['path']).read_bytes() == Path('src/tests/fixtures/empty.mp3').read_bytes()
