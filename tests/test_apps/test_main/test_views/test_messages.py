import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def messages(mixer, faker):
    return mixer.cycle(20).blend(
        'main.Message',
        message_json={
            'text': faker.text(),
            'from': {'id': 123},
            'date': 1670581213,
        },
    )


def test(client, messages):
    response = client.get('/messages')

    assert response.status_code == 200


def test_by_htmx(client, messages):
    response = client.get('/messages', headers={'Hx-Request': 'true'})

    assert response.status_code == 200
