import pytest
from bs4 import BeautifulSoup

from server.apps.main.models import User

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def users(mixer):
    return mixer.cycle(130).blend(User, referrer_id=None)


def test(client, users):
    response = client.get('/users')

    assert response.status_code == 200
    assert len(BeautifulSoup(response.content.decode('utf-8'), 'lxml').find_all('tr')) == 51


def test_by_htmx(client, users):
    response = client.get('/users', headers={'Hx-Request': 'true'})

    assert response.status_code == 200
    assert 'DOCTYPE' not in str(response)
    assert len(BeautifulSoup(response.content.decode('utf-8'), 'lxml').find_all('tr')) == 51


@pytest.mark.parametrize('param', ['comment', '-comment'])
def test_ordering(client, param, users):
    response = client.get(f'/users?order={param}')

    assert response.status_code == 200
    assert list(User.objects.order_by(param).values_list('chat_id', flat=True)[:50]) == [
        int(x.text) for x in BeautifulSoup(response.content.decode('utf-8'), 'lxml').find_all('th', user_id=True)
    ]


def test_filtering(client):
    response = client.get('/users?is_active=true')

    assert response.status_code == 200
    assert list(User.objects.filter(is_active=True).values_list('chat_id', flat=True)[:50]) == [
        int(x.text) for x in BeautifulSoup(response.content.decode('utf-8'), 'lxml').find_all('th', user_id=True)
    ]
