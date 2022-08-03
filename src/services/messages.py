"""Сервисный слой для работы с сообщениями.

Classes:
    Messages
"""
from fastapi import Depends

from integrations.queue_integration import NatsIntegration, QueueIntegrationInterface


class Messages(object):
    """Класс, представляющий сообщения."""

    _queue_integration: QueueIntegrationInterface

    def __init__(self, queue_integration: QueueIntegrationInterface = Depends(NatsIntegration)):
        """Конструктор класса.

        :param queue_integration: QueueIntegrationInterface
        """
        self._queue_integration = queue_integration

    async def delete(self, message_ids: list[int]):
        """Удалить сообщения.

        :param message_ids: list[int]
        """
        await self._queue_integration.send(
            {'message_ids': message_ids},
            'Messages.Deleted',
            1,
        )
