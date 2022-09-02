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

from repositories.auth import UserRepositoryInterface, UserSchema, UserInsertSchema
from repositories.messages import MessageRepositoryInterface
from repositories.notification import NotificationRepositoryInterface
from repositories.user_action import UserActionRepositoryInterface, UserActionSchema, UserActionEnum


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
        js = nats_client.jetstream()

        logger.info('Publishing to queue: {0}, event_id: {1}'.format(self._queue_name, event['event_id']))
        await js.publish(self._queue_name, json.dumps(event).encode('utf-8'))
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
        js = nats_client.jetstream()
        await js.subscribe('default', durable='quranbot_admin', cb=self._message_handler)
        while True:  # noqa: WPS457
            await asyncio.sleep(1)

    async def _message_handler(self, msg):
        await msg.ack()
        event_dict = json.loads(msg.data.decode())
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


class MessageCreatedEvent(object):
    """Событие создания сообщений."""

    event_name = 'Messages.Created'

    def __init__(
        self,
        messages_repository: MessageRepositoryInterface,
    ):
        """Конструктор класса.

        :param messages_repository: NotificationRepositoryInterface
        """
        self._messages_repository = messages_repository

    async def handle_event(self, event_data):
        """Обработка события.

        :param event_data: dict
        """
        await self._messages_repository.save_messages(event_data['messages'])


class UserSubscribedEvent(object):
    """Событие подписки нового пользователя."""

    event_name = 'User.Subscribed'

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        user_action_repository: UserActionRepositoryInterface,
    ):
        """Конструктор класса.

        :param user_action_repository: NotificationRepositoryInterface
        """
        self._user_action_repository = user_action_repository
        self._user_repository = user_repository

    async def handle_event(self, event_data):
        """Обработка события.

        :param event_data: dict
        """
        await self._user_repository.create(UserInsertSchema(
            chat_id=event_data['user_id'],
            day=2,
        ))
        await self._user_action_repository.save(UserActionSchema(
            user_action_id=uuid.uuid4(),
            date_time=event_data['date_time'],
            action=UserActionEnum.subscribed,
            user_id=event_data['user_id']
        ))


class UserUnsubscribedEvent(object):
    """Событие создания действия пользователя."""

    event_name = 'User.Unsubscribed'

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        user_action_repository: UserActionRepositoryInterface,
    ):
        """Конструктор класса.

        :param user_action_repository: NotificationRepositoryInterface
        """
        self._user_action_repository = user_action_repository
        self._user_repository = user_repository

    async def handle_event(self, event_data):
        """Обработка события.

        :param event_data: dict
        """
        await self._user_repository.update_status(event_data['user_id'], to=False)
        await self._user_action_repository.save(UserActionSchema(
            user_action_id=uuid.uuid4(),
            date_time=event_data['date_time'],
            action=UserActionEnum.unsubscribed,
            user_id=event_data['user_id']
        ))


class UserReactivatedEvent(object):
    """Событие создания действия пользователя."""

    event_name = 'User.Reactivated'

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        user_action_repository: UserActionRepositoryInterface,
    ):
        """Конструктор класса.

        :param user_action_repository: NotificationRepositoryInterface
        """
        self._user_action_repository = user_action_repository
        self._user_repository = user_repository

    async def handle_event(self, event_data):
        """Обработка события.

        :param event_data: dict
        """
        await self._user_repository.update_status(event_data['user_id'], to=True)
        await self._user_action_repository.save(UserActionSchema(
            user_action_id=uuid.uuid4(),
            date_time=event_data['date_time'],
            action=UserActionEnum.unsubscribed,
            user_id=event_data['user_id']
        ))


class UserSubscribeWithReferrerEvent(object):
    """Событие создания действия пользователя."""

    event_name = 'User.Reactivated'

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        user_action_repository: UserActionRepositoryInterface,
    ):
        """Конструктор класса.

        :param user_action_repository: NotificationRepositoryInterface
        """
        self._user_action_repository = user_action_repository
        self._user_repository = user_repository

    async def handle_event(self, event_data):
        """Обработка события.

        :param event_data: dict
        """
        await self._user_repository.create(UserInsertSchema(
            chat_id=event_data['user_id'],
            day=2,
        ))
        await self._user_action_repository.save(UserActionSchema(
            user_action_id=uuid.uuid4(),
            date_time=event_data['date_time'],
            action=UserActionEnum.unsubscribed,
            user_id=event_data['user_id']
        ))
