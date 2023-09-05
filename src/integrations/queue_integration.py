"""Интеграция с шиной сообщений.

В кач-ве шины сообщений используется https://nats.io/
Для валидации сообщений, отправляемых в шину и поддержки совместимости используется собственное решение,
основанное на https://json-schema.org/
Репозиторий схем событий - https://github.com/blablatdinov/quranbot-schema-registry

Classes:
    QueueIntegrationInterface
    NatsIntegration
"""


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

    _queue_name = 'quranbot'

    async def send(self, event_data, event_name, version) -> None:
        """Отправить событие.

        :param event_data: dict
        :param event_name: str
        :param version: int
        """


class NatsEvents(object):
    """События из nats."""

    def __init__(self, handlers: list):
        """Конструктор класса.

        :param handlers: list
        """
        self._handlers = handlers

    async def receive(self) -> None:
        """Прием сообщений."""
