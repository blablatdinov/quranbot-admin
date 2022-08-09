"""Интеграция с шиной сообщений.

В кач-ве шины сообщений используется https://nats.io/
Для валидации сообщений, отправляемых в шину и поддержки совместимости используется собственное решение,
основанное на https://json-schema.org/
Репозиторий схем событий - https://github.com/blablatdinov/quranbot-schema-registry

Classes:
    QueueIntegrationInterface
    NatsIntegration
"""
import asyncio
import datetime
import json
import uuid

import nats
from aioredis.client import Redis
from loguru import logger
from quranbot_schema_registry import validate_schema

from repositories.notification import NotificationRepositoryInterface


class QueueIntegrationInterface(object):
    """Интерфейс интеграции с шиной событий."""

    async def send(self, event: dict, event_name: str, version: int):
        """Отправить событие.

        :param event: dict
        :param event_name: str
        :param version: int
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class NatsIntegration(QueueIntegrationInterface):
    """Интеграция с nats."""

    _queue_name = 'default'

    async def send(self, event_data, event_name, version) -> None:
        """Отправить событие.

        :param event_data: dict
        :param event_name: str
        :param version: int
        """
        event = {
            'event_id': str(uuid.uuid4()),
            'event_version': version,
            'event_name': event_name,
            'event_time': str(datetime.datetime.now()),
            'producer': 'quranbot-admin',
            'data': event_data,
        }
        validate_schema(event, event_name, version)
        nats_client = await nats.connect('localhost')

        logger.info('Publishing to queue: {0}, event_id: {1}'.format(self._queue_name, event['event_id']))
        await nats_client.publish(self._queue_name, json.dumps(event).encode('utf-8'))
        logger.info('Event: {0} to queue: {1} successful published'.format(event['event_id'], self._queue_name))
        await nats_client.close()


class NatsEvents(object):
    """События из nats."""

    def __init__(self, handlers: list):
        """Конструктор класса.

        :param handlers: list
        """
        self._handlers = handlers

    async def receive(self) -> None:
        """Прием сообщений."""
        nats_client = await nats.connect('localhost')
        logger.info('Start handling events...')
        logger.info('Receive evenst list: {0}'.format([event_handler.event_name for event_handler in self._handlers]))
        await nats_client.subscribe('default', cb=self._message_handler)
        while True:  # noqa: WPS457
            await asyncio.sleep(1)

    async def _message_handler(self, event):
        event_dict = json.loads(event.data.decode())
        event_log_data = 'event_id={0} event_name={1}'.format(event_dict['event_id'], event_dict['event_name'])
        logger.info('Event {0} received'.format(event_log_data))
        try:
            validate_schema(event_dict, event_dict['event_name'], event_dict['event_version'])
        except TypeError as event_validate_error:
            logger.error('Validate {0} failed {1}'.format(event_log_data, str(event_validate_error)))
            return

        for event_handler in self._handlers:
            if event_handler.event_name == event_dict['event_name']:
                logger.info('Handling {0} event...'.format(event_log_data))
                await event_handler.handle_event(event_dict['data'])
                logger.info('Event {0} handled successful'.format(event_log_data))
                return

        logger.info('Event {0} skipped because not find handler'.format(event_log_data))


class NotificationCreatedEvent(object):
    """Событие создания уведомления."""

    event_name = 'Notification.Created'
    _redis: Redis

    def __init__(
        self,
        redis: Redis,
        nats_integration: QueueIntegrationInterface,
        notification_repository: NotificationRepositoryInterface,
    ):
        """Конструктор класса.

        :param redis: Redis
        :param nats_integration: QueueIntegrationInterface
        :param notification_repository: NotificationRepositoryInterface
        """
        self._redis = redis
        self._nats_integration = nats_integration
        self._notification_repository = notification_repository

    async def handle_event(self, event_data):
        """Обработка события.

        :param event_data: dict
        """
        # TODO: saving in database if user has not connection by websocket
        await self._notification_repository.create(event_data['public_id'], event_data['text'])
        await self._nats_integration.send(event_data, 'Websocket.NotificationCreated', 1)
