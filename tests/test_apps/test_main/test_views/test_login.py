import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def user(mixer):
    new_user = mixer.blend('main.User', referrer_id=None, is_active=True)
    new_user.set_password('simple')
    new_user.save()
    return new_user


def test_page(client):
    response = client.get('/login')

    assert response.status_code == 200


def test_login(client, user):
    response = client.post(
        '/login',
        {
            'username': user.username,
            'password': 'simple',
        },
    )

    assert response.status_code == 302
    assert response.headers['Location'] == '/ayats'


def test_fail_auth(client, user):
    response = client.post(
        '/login',
        {
            'username': user.username,
            'password': 'invalid',
        },
    )

    assert response.status_code == 302
    assert response.headers['Location'] == '/login'
