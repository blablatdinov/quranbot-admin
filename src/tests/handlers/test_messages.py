import datetime

import pytest

from handlers.v1.schemas.messages import Message
from main import app
from repositories.ayat import ElementsCount
from repositories.paginated_sequence import PaginatedSequence, PaginatedSequenceInterface
from tests.handlers.test_ayats import ElementsCountMock


class PaginatedSequenceMock(PaginatedSequenceInterface):

    def update_query(self, query: str):
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


app.dependency_overrides[ElementsCount] = ElementsCountMock
app.dependency_overrides[PaginatedSequence] = PaginatedSequenceMock


def test_get_list(client):
    got = client.get('/api/v1/messages')

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert list(got.json()['results'][0].keys()) == ['id', 'message_source', 'sending_date', 'message_id', 'text']


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
    got = client.delete('/api/v1/messages/34/delete-from-chat')

    assert got.status_code == 204
