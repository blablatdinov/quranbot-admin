from fastapi import Depends

from integrations.queue_integration import QueueIntegrationInterface, NatsIntegration


class Mailing(object):

    _queue_integration: QueueIntegrationInterface

    def __init__(self, queue_integration: NatsIntegration = Depends()):
        self._queue_integration = queue_integration

    async def create(self, text: str):
        await self._queue_integration.send(text)
