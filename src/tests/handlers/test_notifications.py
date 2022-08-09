import uuid

import pytest

from integrations.queue_integration import NatsIntegration, QueueIntegrationInterface
from main import app
from repositories.notification import (
    NotificationInsertQueryResult,
    NotificationRepository,
    NotificationRepositoryInterface,
    NotificationResponseSchema,
)


class NotificationRepositoryMock(NotificationRepositoryInterface):

    async def get_notifications(self):
        return [NotificationResponseSchema(uuid=uuid.uuid4(), text='some text')]

    async def create(self, text):
        return NotificationInsertQueryResult(uuid=uuid.uuid4(), text='some text')


class QueueIntegrationMock(QueueIntegrationInterface):

    async def send(self, event: dict, event_name: str, version: int):
        pass


@pytest.fixture()
def override_dependencies():
    app.dependency_overrides[NotificationRepository] = NotificationRepositoryMock
    app.dependency_overrides[NatsIntegration] = QueueIntegrationMock


def test_get(client, override_auth_dep, override_dependencies):
    got = client.get('/api/v1/notifications/')

    assert got.status_code == 200
    assert isinstance(got.json(), list)
    assert list(got.json()[0].keys()) == ['uuid', 'text']


def test_create(client, override_auth_dep, override_dependencies):
    got = client.post('/api/v1/notifications/', json={
        'text': 'hello',
    })

    assert got.status_code == 201
