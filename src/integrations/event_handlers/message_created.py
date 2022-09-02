"""Модуль, содержащий обработчик события из очереди сообщений.

Classes:
    MessageCreatedEvent
"""
from repositories.messages import MessageRepositoryInterface


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
