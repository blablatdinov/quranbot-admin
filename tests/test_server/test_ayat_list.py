import pytest
from bs4 import BeautifulSoup

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def ayats(mixer):
    return mixer.cycle(230).blend('main.Ayat')


def test_ayat_list(client, ayats):
    got = client.get('/ayats')
    links = BeautifulSoup(str(got.content).replace('\\n', ''), 'lxml').find('ul', class_='pagination').find_all('a')

    assert got.status_code == 200
    assert [list_elem.attrs for list_elem in links] == [
        {
            'class': [
                'page-link',
                'active',
            ],
            'href': '?page=1',
            'hx-get': '/ayats?page=1',
            'hx-replace-url': '/ayats?page=1',
            'hx-target': '#ayats-list',
        },
        {
            'class': [
                'page-link',
            ],
            'href': '?page=2',
            'hx-get': '/ayats?page=2',
            'hx-replace-url': '/ayats?page=2',
            'hx-target': '#ayats-list',
        },
        {
            'class': [
                'page-link',
            ],
            'href': '?page=3',
            'hx-get': '/ayats?page=3',
            'hx-replace-url': '/ayats?page=3',
            'hx-target': '#ayats-list',
        },
        {
            'class': [
                'page-link',
            ],
            'href': '?page=2',
            'hx-get': '/ayats?page=2',
            'hx-replace-url': '/ayats?page=2',
            'hx-target': '#ayats-list',
        },
        {
            'class': [
                'page-link',
            ],
            'href': '?page=1',
            'hx-get': '/ayats?page=5',
            'hx-replace-url': '/ayats?page=5',
            'hx-target': '#ayats-list',
        },
    ]
    assert [list_elem.text for list_elem in links] == ['1', '2', '3', '\\xc2\\xbb', '\\xe2\\x87\\xa5']


def test_ayat_list_middle_page(client, ayats):
    got = client.get('/ayats?page=3')

    assert got.status_code == 200


def test_by_htmx(client, ayats):
    got = client.get('/ayats?page=3', headers={'Hx-Request': 'true'})

    assert got.status_code == 200
