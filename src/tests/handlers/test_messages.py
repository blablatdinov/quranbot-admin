import datetime

import pytest
from fastapi import Header

from app_types.query import QueryInterface
from handlers.v1.schemas.messages import Message
from integrations.queue_integration import NatsIntegration, QueueIntegrationInterface
from main import app
from repositories.auth import UserSchema
from repositories.ayat import ElementsCount
from repositories.paginated_sequence import PaginatedSequence, PaginatedSequenceInterface
from services.auth import User
from tests.handlers.test_ayats import ElementsCountMock


class PaginatedSequenceMock(PaginatedSequenceInterface):

    def update_query(self, query: QueryInterface):
        return self

    def update_model_to_parse(self, model_to_parse):
        return self

    async def get(self):
        return [
            Message(
                id=1,
                message_source=123,
                sending_date=datetime.datetime(2022, 4, 5),
                message_id=435,
                text='text',
            ),
        ]


class UserMock(object):

    @classmethod
    def get_from_token(cls, _: str = Header(..., alias='Authorization')):
        return UserSchema(id=1, username='user', password='1')  # noqa: S106


class QueueMock(QueueIntegrationInterface):

    async def send(self, event: dict, event_name: str, version: int):
        pass


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[ElementsCount] = ElementsCountMock
    app.dependency_overrides[PaginatedSequence] = PaginatedSequenceMock
    app.dependency_overrides[NatsIntegration] = QueueMock


app.dependency_overrides[User.get_from_token] = UserMock.get_from_token


def test_get_list(client):
    got = client.get('/api/v1/messages')
    payload = got.json()['results']

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert list(payload[0].keys()) == [
        'id',
        'message_source',
        'sending_date',
        'message_id',
        'text',
    ]


def test_get_message(client):
    got = client.get('/api/v1/messages/34')

    assert got.status_code == 200
    assert got.json() == {
        'id': 34,
        'message_id': 1,
        'message_source': 'from 23343',
        'sending_date': '1000-01-01T00:00:00',
        'text': 'Hello...',
    }


def test_delete_message_from_telegram(client):
    got = client.delete('/api/v1/messages/', json={
        'message_ids': [1, 2, 3],
    })

    assert got.status_code == 201
