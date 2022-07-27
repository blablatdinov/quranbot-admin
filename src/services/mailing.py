from fastapi import Depends

from integrations.queue_integration import NatsIntegration, QueueIntegrationInterface


class Mailing(object):
    """Рассылка."""

    _queue_integration: QueueIntegrationInterface

    def __init__(self, queue_integration: NatsIntegration = Depends()):
        self._queue_integration = queue_integration

    async def create(self, text: str):
        """Создание.

        :param text: str
        """
        await self._queue_integration.send(
            {'text': text},
            'Mailing.Created',
            1,
        )
