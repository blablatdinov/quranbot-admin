import pytest
from fastapi import Header
from fastapi.testclient import TestClient
from httpx._models import Headers  # noqa: WPS436

from integrations.queue_integration import NatsIntegration, QueueIntegrationInterface
from main import app
from repositories.auth import UserSchema
from services.auth import User


@pytest.fixture()
def client():
    http_client = TestClient(app)
    http_client.headers = Headers({'Authorization': ''})
    return http_client


class UserMock(object):

    @classmethod
    def get_from_token(cls, _: str = Header(..., alias='Authorization')):
        return UserSchema(chat_id=1, username='user', password='1')  # noqa: S106


class QueueIntegrationMock(QueueIntegrationInterface):

    async def send(self, event_data, event_name, version):
        pass


@pytest.fixture()
def override_auth_dep():
    app.dependency_overrides[User.get_from_token] = UserMock.get_from_token


@pytest.fixture()
def override_queue_dep():
    app.dependency_overrides[NatsIntegration] = QueueIntegrationMock
