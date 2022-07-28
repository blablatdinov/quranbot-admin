from fastapi import Depends

from integrations.queue_integration import QueueIntegrationInterface, NatsIntegration


class Messages(object):

    _queue_integration: QueueIntegrationInterface

    def __init__(self, queue_integration: QueueIntegrationInterface = Depends(NatsIntegration)):
        self._queue_integration = queue_integration

    async def delete(self, message_ids: list[int]):
        await self._queue_integration.send(
            {'message_ids': message_ids},
            'Messages.Deleted',
            1,
        )
