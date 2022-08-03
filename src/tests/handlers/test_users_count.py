import datetime

import pytest

from main import app
from repositories.paginated_sequence import ElementsCount, ElementsCountInterface
from repositories.user_action import (
    ActionCountMapQueryResult,
    QueryResult,
    UserActionRepository,
    UserActionRepositoryInterface,
)


class UserActionRepositoryMock(UserActionRepositoryInterface):

    async def get_action_count_map_until_date(self, date: datetime.date):
        return ActionCountMapQueryResult(
            subscribed=1,
            unsubscribed=2,
            reactivated=8,
        )

    async def get_user_actions_by_date_range(self, start_date: datetime.date, finish_date: datetime.date):
        return [QueryResult(date=datetime.date(2020, 1, 1), action='subscribed')]


class ElementsCountMock(ElementsCountInterface):

    def update_query(self, query: str) -> ElementsCountInterface:
        return self

    async def get(self):
        return 4


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[ElementsCount] = ElementsCountMock
    app.dependency_overrides[UserActionRepository] = UserActionRepositoryMock


def test(client):
    got = client.get('/api/v1/users/graph-data/')

    assert got.status_code == 200


def test_users_count(client):
    got = client.get('/api/v1/users/count-github-badge/')

    assert got.status_code == 200
