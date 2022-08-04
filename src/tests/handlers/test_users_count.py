import datetime

import pytest

from main import app
from repositories.paginated_sequence import ElementsCount, ElementsCountInterface
from repositories.user_action import (
    ActionCountMapQueryResult,
    ActionsByDateRangeQueryResult,
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
        return [ActionsByDateRangeQueryResult(date=datetime.date(2020, 1, 1), action='subscribed')]


class ElementsCountMock(ElementsCountInterface):

    def update_query(self, query: str) -> ElementsCountInterface:
        return self

    async def get(self):
        return 4


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[ElementsCount] = ElementsCountMock
    app.dependency_overrides[UserActionRepository] = UserActionRepositoryMock


def test(client, override_auth_dep):
    got = client.get('/api/v1/users/graph-data/')

    assert got.status_code == 200


def test_users_graph_data_invalid_input(client, override_auth_dep):
    got = client.get('/api/v1/users/graph-data/?start_date=2020-07-02')

    assert got.json() == {
        'detail': [
            {
                'ctx': {
                    'limit_value': '2020-07-29',
                },
                'loc': [
                    'query',
                    'start_date',
                ],
                'msg': 'start date must be greater than 2020-07-09',
                'type': 'value_error.date.not_ge',
            },
        ],
    }


def test_users_count(client):
    got = client.get('/api/v1/users/count-github-badge/')

    assert got.status_code == 200
