import pytest

from main import app
from repositories.paginated_sequence import ElementsCount, ElementsCountInterface


class ElementsCountMock(ElementsCountInterface):

    def __init__(self, input_value: int):
        self._input_value = input_value

    async def get(self):
        return self._input_value


@pytest.fixture()
def override_dependency():
    app.dependency_overrides[ElementsCount] = ElementsCountMock


def test(client):
    got = client.get('/api/v1/users/graph-data/')

    assert got.status_code == 200


def test_users_count(client):
    got = client.get('/api/v1/users/count-github-badge/')

    assert got.status_code == 200
