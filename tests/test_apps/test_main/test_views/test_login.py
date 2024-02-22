import pytest

pytestmark = [pytest.mark.django_db]


@pytest.fixture()
def user(mixer):
    new_user = mixer.blend('main.User', referrer_id=None, is_active=True)
    new_user.set_password('simple')
    new_user.save()
    return new_user


def test_page(anon):
    response = anon.get('/login')

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


def test_invalid_password(anon, user):
    response = anon.post(
        '/login',
        {
            'username': user.username,
            'password': 'invalid',
        },
    )

    assert response.status_code == 401
    assert 'Пароль не верен' in response.content.decode('utf-8')


def test_invalid_username(anon, user):
    response = anon.post(
        '/login',
        {
            'username': 'NotFoundable',
            'password': 'invalid',
        },
    )

    assert response.status_code == 401
    assert 'Пользователь не найден' in response.content.decode('utf-8')
