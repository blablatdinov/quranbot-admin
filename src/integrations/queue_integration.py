class QueueIntegrationInterface(object):

    async def send(self, text):
        raise NotImplementedError


class NatsIntegration(QueueIntegrationInterface):

    async def send(self, text):
        print(text)
