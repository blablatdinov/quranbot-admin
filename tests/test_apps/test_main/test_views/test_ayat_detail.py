import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def ayat(mixer):
    return mixer.blend('main.Ayat')


def test(client, ayat):
    response = client.get('/ayats/{0}'.format(ayat.public_id))

    assert response.status_code == 200


def test_post(client, ayat):
    response = client.post('/ayats/{0}'.format(ayat.public_id))

    assert response.status_code == 200
    assert '<html>' not in str(response.content)
