import datetime

import pytest

from main import app
from repositories.messages import MessageRepository, MessageRepositoryInterface
from handlers.v1.schemas.messages import MessageGraphDataItem


class MessageRepositoryMock(MessageRepositoryInterface):
    
    async def get_messages_for_graph(self, start_date, finish_date):
        return [MessageGraphDataItem(date=datetime.date(2022, 8, 6), messages_count=1)]


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[MessageRepository] = MessageRepositoryMock


def test(client):
    got = client.get('/api/v1/messages/count-graph/')

    payload = got.json()

    assert got.status_code == 200
    assert isinstance(payload, list)
    assert list(payload[0].keys()) == ['date', 'messages_count']
