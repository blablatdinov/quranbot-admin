import json

import pika
import pytest
from bs4 import BeautifulSoup
from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def _failed_events():
    connection = pika.BlockingConnection(
        pika.URLParameters(
            'amqp://{0}:{1}@{2}:5672/{3}'.format(
                settings.RABBITMQ_USER,
                settings.RABBITMQ_PASS,
                settings.RABBITMQ_HOST,
                settings.RABBITMQ_VHOST,
            ),
        ),
    )
    channel = connection.channel()
    channel.queue_declare(queue='failed-events', durable=True)
    channel.queue_purge('failed-events')
    channel.basic_publish(
        exchange='',
        routing_key='failed-events',
        body=json.dumps({
            'event_id': 'e5ca6719-7ba4-4907-b563-bed4e4d647e3',
            'event_version': 1,
            'event_name': 'Messages.Created',
            'event_time': '1710084838',
            'producer': 'quranbot',
        }),
    )


@pytest.mark.usefixtures('_failed_events')
def test_get(client):
    response = client.get('/failed-events')

    assert response.status_code == 200
    assert [
        str(x) for x in BeautifulSoup(response.content.decode('utf-8')).find('tbody').find_all('tr')[0].find_all('td')
    ] == [
        '<td>Messages.Created</td>',
        '<td>10 Мар 2024 15:33:58</td>',
        '<td>1</td>',
        '\n'.join([
            '<td>',
            '<pre style="width: 600px; overflow-y: auto">{',
            '  "event_id": "e5ca6719-7ba4-4907-b563-bed4e4d647e3",',
            '  "event_version": 1,',
            '  "event_name": "Messages.Created",',
            '  "event_time": "1710084838",',
            '  "producer": "quranbot"',
            '}</pre>',
            '</td>',
        ]),
        ''.join([
            '<td>\n',
            '<a',
            ' class="btn btn-primary"',
            ' href="/failed-events/e5ca6719-7ba4-4907-b563-bed4e4d647e3/resolved"',
            ' hx-get="/failed-events/e5ca6719-7ba4-4907-b563-bed4e4d647e3/resolved"',
            ' hx-target="#failed-events-table"',
            '>Решено</a>\n',
            '</td>',
        ]),
    ]


@pytest.mark.usefixtures('_failed_events')
def test_mark_resolved(client):
    client.get('/failed-events')
    response = client.post('/failed-events/{0}/resolved'.format('e5ca6719-7ba4-4907-b563-bed4e4d647e3'))

    assert response.status_code == 200
    assert len(BeautifulSoup(response.content.decode('utf-8')).find('tbody').find_all('tr')) == 0
