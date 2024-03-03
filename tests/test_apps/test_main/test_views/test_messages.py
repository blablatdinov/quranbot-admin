import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def messages(mixer):
    return mixer.cycle(20).blend('main.Message', message_json={'text': '', 'from': {'id': 123}})


def test(client, messages):
    response = client.get('/messages')

    assert response.status_code == 200


def test_by_htmx(client, messages):
    response = client.get('/messages', headers={'Hx-Request': 'true'})

    assert response.status_code == 200
