"""Модуль, содержащий обработчик события из очереди сообщений.

Classes:
    NotificationCreatedEvent
"""
from redis.asyncio import Redis

from integrations.queue_integration import QueueIntegrationInterface
from repositories.notification import NotificationRepositoryInterface


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
