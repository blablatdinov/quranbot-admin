import json
import random
from itertools import cycle, islice

import pika
import pytest
from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def event_reader():
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
    channel.queue_declare(queue='quranbot.mailings')
    channel.queue_purge('quranbot.mailings')

    def _event_reader(queue_name):
        method_frame, _, body = channel.basic_get(queue_name)
        decoded_body = json.loads(body.decode('utf-8'))
        channel.basic_ack(method_frame.delivery_tag)
        return decoded_body

    return _event_reader


@pytest.fixture
def user(mixer):
    return mixer.blend('main.User', referrer_id=None)


@pytest.fixture
def mailings(mixer, user):
    mailings = mixer.cycle(5).blend('main.Mailing')
    mixer.cycle(40).blend(
        'main.Message',
        message_json=({'chat': {'id': random.randint(1000, 9999)}} for _ in range(40)),  # noqa: S311 not secure issue
        mailing=(x for x in islice(cycle(mailings), 40)),
        from_id=user.chat_id,
    )
    return mailings


def test_mailings(client, mailings):
    response = client.get('/mailings')

    assert response.status_code == 200


def test_mailing_form(client):
    response = client.get('/mailings/new')

    assert response.status_code == 200


def test_create_mailing(client, event_reader):
    response = client.post(
        '/mailings',
        {
            'group': 'admins',
            'text': 'Hello',
        },
    )
    event = event_reader('quranbot.mailings')

    assert response.status_code == 200
    assert event['event_name'] == 'Mailing.Created'
    assert event['event_version'] == 1
    assert event['data'] == {
        'text': 'Hello',
        'group': 'admins',
    }


def test_delete_mailing(client, mailings):
    response = client.get('/mailings/{0}/delete'.format(mailings[0].mailing_id))

    assert response.status_code == 200
