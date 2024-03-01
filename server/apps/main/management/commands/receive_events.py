"""Receiving events."""

import json
import logging
import time
from typing import Any

import pika
from django.conf import settings
from django.core.management.base import BaseCommand
from quranbot_schema_registry import validate_schema

from server.apps.main.models import Message, User, UserAction

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
                handler(channel, method_frame, decoded_body)

    def _handle_updates_log(
        self,
        channel: pika.channel.Channel,
        method_frame: pika.spec.Basic.GetOk,
        decoded_body: dict,  # type: ignore [type-arg]
    ) -> None:
        for message in decoded_body['data']['messages']:
            Message.objects.create(
                message_id=json.loads(message['message_json'])['message_id'],
                message_json=message['message_json'],
                is_unknown=message['is_unknown'],
                trigger_message_id=message['trigger_message_id'],
            )
        channel.basic_ack(method_frame.delivery_tag)

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
                chat_id=decoded_body['data']['user_id'],
            )
            UserAction.objects.create(
                date_time=decoded_body['data']['date_time'],
                action='Reactivated',
                user_id=decoded_body['data']['user_id'],
            )
        channel.basic_ack(method_frame.delivery_tag)
