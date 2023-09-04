import pytest


@pytest.fixture()
async def user(pgsql):
    query = """
        INSERT INTO users (chat_id, username, password_hash)
        VALUES (123, 'me', 'PYJ8Ug4L9xd..QmScF7rVCcqBMoKrpaqlMfkDn3uvL8')
    """
    await pgsql.execute(query)


async def test(migrate, client, user):
    got = client.post('/api/v1/auth/', data={
        'username': 'me',
        'password': 'qwerty',
    })

    print(got.json())
    assert got.status_code == 201
