import pytest
from jose import jwt

from settings import settings


@pytest.fixture()
async def user(pgsql):
    query = """
        INSERT INTO users (chat_id, username, password_hash)
        VALUES (123, 'me', 'PYJ8Ug4L9xd..QmScF7rVCcqBMoKrpaqlMfkDn3uvL8')
    """
    await pgsql.execute(query)


async def test(migrate, client, user, freezer):
    freezer.move_to('2023-09-04')
    got = client.post('/api/v1/auth/', data={
        'username': 'me',
        'password': 'qwerty',
    })

    assert got.status_code == 201
    assert list(got.json().keys()) == ['access_token', 'token_type']
    assert jwt.decode(
        got.json()['access_token'],
        settings.JWT_SECRET,
        algorithms=[settings.JWT_ALGORITHM],
    ) == {
        'exp': 1693789200,
        'iat': 1693785600,
        'nbf': 1693785600,
        'sub': '123',
        'user': {
            'chat_id': 123,
            'password': 'PYJ8Ug4L9xd..QmScF7rVCcqBMoKrpaqlMfkDn3uvL8',
            'username': 'me'
        },
    }
