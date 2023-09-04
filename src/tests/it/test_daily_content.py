import json

import pika

from settings import settings


def test(client, pgsql):
    got = client.get('/api/v1/daily-content/last-registered-day/')

    assert got.status_code == 200
    assert got.json() == {'day_num': 774}


async def test_create(client, pgsql):
    got = client.post('/api/v1/daily-content/', json={
        'day_num': 775,
        'ayat_ids': [1, 2, 3],
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

    assert got.status_code == 201
    assert [
        {'ayat_id': row['ayat_id'], 'day': row['day']}
        for row in await pgsql.fetch_all('SELECT ayat_id, day FROM ayats WHERE ayat_id in (1, 2, 3)')
    ] == [
        {'ayat_id': 1, 'day': 775},
        {'ayat_id': 3, 'day': 775},
        {'ayat_id': 2, 'day': 775},
    ]
    assert published_event == {
        'event_id': 'some_id',
        'event_name': 'event_name',
        'event_time': '392409283',
        'event_version': 1,
        'producer': 'some producer',
        'data': {
            'ayat_ids': [1, 2, 3],
            'day': 775,
        },
    }
