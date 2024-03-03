"""Receiving events."""

import json
import logging
import time
import datetime
from typing import Any

import pika
from django.conf import settings
from django.core.management.base import BaseCommand
from quranbot_schema_registry import validate_schema
from django.db.utils import IntegrityError
from django.db import transaction

from server.apps.main.models import Message, User, UserAction, CallbackData

logger = logging.getLogger('django')


class Command(BaseCommand):
    """Receiving events."""

    def handle(  # type: ignore [misc]
        self,
        *args: list[str],
        **options: Any,  # noqa: ANN401
    ) -> None:  # noqa: ANN002, ANN003
        """Receiving events."""
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
        handlers = {
            'updates_log': self._handle_updates_log,
            'users': self._handle_users,
        }
        while True:
            time.sleep(1)
            for queue_name, handler in handlers.items():
                method_frame, _, body = channel.basic_get(queue_name)
                if not body:
                    continue
                logger.info('Taked event: {0}'.format(body))
                decoded_body = json.loads(body.decode('utf-8'))
                try:
                    validate_schema(
                        decoded_body,
                        decoded_body['event_name'],
                        decoded_body['event_version'],
                    )
                except (TypeError, KeyError) as err:
                    logger.exception(
                        'Schema of event: {0} invalid. {1}'.format(
                            decoded_body['event_id'],
                            str(err),  # noqa: TRY401
                        ),
                    )
                try:
                    with transaction.atomic():
                        handler(channel, method_frame, decoded_body)
                except Exception:
                    logger.exception('{0} process failed, push to failed-events queue'.format(
                        decoded_body['event_id'],
                    ))
                    channel.basic_publish(
                        exchange='',
                        routing_key='failed-events',
                        body=body,
                    )
                channel.basic_ack(method_frame.delivery_tag)

    def _handle_updates_log(
        self,
        channel: pika.channel.Channel,
        method_frame: pika.spec.Basic.GetOk,
        decoded_body: dict,  # type: ignore [type-arg]
    ) -> None:
        if decoded_body['event_name'] == 'Messages.Created':
            for message in decoded_body['data']['messages']:
                try:
                    Message.objects.create(
                        message_id=json.loads(message['message_json'])['message_id'],
                        message_json=message['message_json'],
                        is_unknown=message['is_unknown'],
                        trigger_message_id=message['trigger_message_id'],
                        trigger_callback_id=message['trigger_callback_id'],
                    )
                except IntegrityError:
                    pass
        elif decoded_body['event_name'] == 'Button.Pushed':
            CallbackData.objects.create(
                callback_id=int(json.loads(decoded_body['data']['json'])['callback_query']['id']),
                date_time=datetime.datetime.fromisoformat(decoded_body['data']['timestamp']),
                user_id=json.loads(decoded_body['data']['json'])['callback_query']['from']['id'],
                json=decoded_body['data']['json'],
            )
            decoded_body['data']

    def _handle_users(
        self,
        channel: pika.channel.Channel,
        method_frame: pika.spec.Basic.GetOk,
        decoded_body: dict,  # type: ignore [type-arg]
    ) -> None:
        if decoded_body['event_name'] == 'User.Reactivated':
            UserAction.objects.create(
                date_time=decoded_body['data']['date_time'],
                action='Reactivated',
                user_id=decoded_body['data']['user_id'],
            )
        elif decoded_body['event_name'] == 'User.Subscribed':
            User.objects.create(
                username=decoded_body['data']['user_id'],
                chat_id=decoded_body['data']['user_id'],
                date_joined=decoded_body['data']['date_time'],
            )
            UserAction.objects.create(
                date_time=decoded_body['data']['date_time'],
                action='Reactivated',
                user_id=decoded_body['data']['user_id'],
            )
