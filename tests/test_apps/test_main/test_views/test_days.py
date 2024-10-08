import pytest
from bs4 import BeautifulSoup

from server.apps.main.models import Ayat

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def nullday_ayats(mixer):
    return mixer.cycle(8).blend('main.Ayat', day=None)


@pytest.fixture
def ayats(mixer):
    return mixer.cycle(20).blend('main.Ayat')


def test_get(client, ayats, nullday_ayats):
    response = client.get('/days')

    assert response.status_code == 200
    assert [f'ayat-{x.ayat_id}' for x in nullday_ayats] == [
        input_['name']
        for input_ in BeautifulSoup(response.content.decode('utf-8'), 'lxml').find_all(
            'input',
            class_='form-check-input',
        )
    ]


def test_post(client, nullday_ayats):
    post_data = {'day': 14} | {f'ayat-{ayat.ayat_id}': '' for ayat in nullday_ayats[:4]}
    response = client.post(
        '/days',
        post_data,
    )

    assert response.status_code == 200
    assert set(
        Ayat.objects.filter(ayat_id__in=[a.ayat_id for a in nullday_ayats[:4]]).values_list('day', flat=True),
    ) == {14}
