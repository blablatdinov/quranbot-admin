import pytest

from blog.models import Post

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def posts(baker):
    return baker.cycle(10).blend(Post)


def test(client):
    got = client.get('/api/v1/blog/posts/')

    assert got.status_code == 200
