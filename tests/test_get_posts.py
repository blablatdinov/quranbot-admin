import pytest
from bs4 import BeautifulSoup

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def posts(baker):
    return baker.make('blog.Post', _quantity=20)


def test(client, posts):
    got = client.get('/')

    soup = BeautifulSoup(got.content, 'lxml')

    assert got.status_code == 200
    assert [el.text for el in soup.find_all('p')] == [p.name for p in posts]
