import datetime
import json
import time
import uuid
from collections.abc import Generator

import pika
import pytest
from django.conf import settings

from server.apps.main.management.commands.receive_events import receiver
from server.apps.main.models import CallbackData, Message, User, UserAction

pytestmark = [pytest.mark.django_db]


def fake_generator() -> Generator[int, None, None]:
    for _ in range(1):
        yield 1


@pytest.fixture()
def event_publisher():
    def _event_publisher(queue_name, event_data):
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
        for queue in 'users', 'updates_log':
            channel.queue_declare(queue=queue)
        channel.queue_purge(queue_name)
        channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(event_data).encode('utf-8'),
        )

    return _event_publisher


@pytest.fixture()
def user(mixer):
    return mixer.blend(User, referrer_id=None)


def test(event_publisher):
    joined_date = datetime.datetime.now(tz=datetime.UTC)
    event_publisher(
        'users',
        {
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'User.Subscribed',
            'event_time': str(int(time.time())),
            'producer': 'tests',
            'data': {
                'user_id': 845834975,
                'date_time': str(joined_date),
                'referrer_id': None,
            },
        },
    )
    receiver(fake_generator())

    assert list(User.objects.values_list('chat_id', 'date_joined')) == [(845834975, joined_date)]
    assert list(UserAction.objects.values('action', 'date_time', 'user_id')) == [
        {
            'action': 'Reactivated',
            'date_time': joined_date,
            'user_id': 845834975,
        },
    ]


def test_invalid_scheme(event_publisher):
    joined_date = datetime.datetime.now(tz=datetime.UTC)
    event_publisher(
        'users',
        {
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'User.Subscribed',
            'event_time': str(int(time.time())),
            'producer': 'tests',
            'data': {
                'user_id': 845834975,
                'date_time': str(joined_date),
            },
        },
    )
    receiver(fake_generator())

    assert User.objects.count() == 0


def test_user_reactivated(event_publisher, user):
    joined_date = datetime.datetime.now(tz=datetime.UTC)
    event_publisher(
        'users',
        {
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'User.Reactivated',
            'event_time': str(int(time.time())),
            'producer': 'tests',
            'data': {
                'user_id': user.chat_id,
                'date_time': str(joined_date),
                'referrer_id': None,
            },
        },
    )
    receiver(fake_generator())

    assert list(UserAction.objects.values('action', 'date_time', 'user_id')) == [
        {
            'action': 'Reactivated',
            'date_time': joined_date,
            'user_id': user.chat_id,
        },
    ]


def test_message_created(event_publisher):
    event_publisher(
        'updates_log',
        {
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'Messages.Created',
            'event_time': str(int(time.time())),
            'producer': 'tests',
            'data': {
                'messages': [
                    {
                        'message_json': '{"message_id": 1}',
                        'is_unknown': False,
                        'trigger_message_id': None,
                        'trigger_callback_id': None,
                    },
                ],
            },
        },
    )
    receiver(fake_generator())

    assert list(Message.objects.values()) == [
        {
            'message_id': 1,
            'message_json': '{"message_id": 1}',
            'is_unknown': False,
            'trigger_message_id': None,
            'trigger_callback_id': None,
        },
    ]


def test_button_pushed(event_publisher, user):
    date_time = datetime.datetime.now(tz=datetime.UTC)
    event_publisher(
        'updates_log',
        {
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'Button.Pushed',
            'event_time': str(int(time.time())),
            'producer': 'tests',
            'data': {
                'json': {'callback_query': {'id': 239874, 'from': {'id': user.chat_id}}},
                'timestamp': str(date_time),
            },
        },
    )
    receiver(fake_generator())

    assert list(CallbackData.objects.values()) == [
        {
            'callback_id': 239874,
            'date_time': date_time,
            'json': {
                'callback_query': {
                    'from': {
                        'id': user.chat_id,
                    },
                    'id': 239874,
                },
            },
            'user_id': user.chat_id,
        },
    ]


def test_fail_event(event_publisher, user):
    joined_date = datetime.datetime.now(tz=datetime.UTC)
    event_publisher(
        'users',
        {
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'User.Subscribed',
            'event_time': str(int(time.time())),
            'producer': 'tests',
            'data': {
                'user_id': user.chat_id,
                'date_time': str(joined_date),
                'referrer_id': None,
            },
        },
    )
    receiver(fake_generator())
