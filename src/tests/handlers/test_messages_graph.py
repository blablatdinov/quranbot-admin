import datetime

import pytest

from main import app
from repositories.messages import MessageRepository, MessageRepositoryInterface


class MessageRepositoryMock(MessageRepositoryInterface):

    async def get_messages_for_graph(self, start_date, finish_date):
        return {datetime.date(2022, 8, 6): 1}


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[MessageRepository] = MessageRepositoryMock


def test(client):
    got = client.get('/api/v1/messages/count-graph/')

    payload = got.json()

    assert got.status_code == 200
    assert isinstance(payload, list)
    assert list(payload[0].keys()) == ['date', 'messages_count']


def test_time_range(client):
    got = client.get('/api/v1/messages/count-graph/?start_date=2022-08-06&finish_date=2022-09-06')

    payload = got.json()

    assert len(payload) == 32
    assert payload[0]['date'] == '2022-08-06'
    assert payload[-1]['date'] == '2022-09-06'
