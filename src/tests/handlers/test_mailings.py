from integrations.queue_integration import NatsIntegration, QueueIntegrationInterface
from main import app


class QueueIntegrationMock(QueueIntegrationInterface):

    async def send(self, event: dict, event_name: str, version: int):
        pass


app.dependency_overrides[NatsIntegration] = QueueIntegrationMock


def test_get_mailings(client):
    got = client.get('/api/v1/mailings')

    assert got.status_code == 200


def test_delete_mailing_from_telegram(client):
    got = client.delete('/api/v1/mailings/23')

    assert got.status_code == 201


def test_create_mailing(client):
    got = client.post('/api/v1/mailings/', json={
        'text': 'some text',
    })

    assert got.status_code == 201
