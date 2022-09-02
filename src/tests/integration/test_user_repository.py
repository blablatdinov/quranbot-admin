import pytest
from pypika import Parameter, Query, Table

from exceptions import UserNotFoundError
from repositories.auth import UserRepository


@pytest.fixture
async def user(db_session):
    user_table = Table('users')
    columns = (
        'chat_id',
        'username',
        'password_hash',
        'is_active',
    )
    parameters = [Parameter(':{0}'.format(field)) for field in columns]
    await db_session.execute(
        str(
            Query()
            .into(user_table)
            .columns(*columns)
            .insert(*parameters),
        ),
        {
            'chat_id': 123,
            'username': 'asdf',
            'password_hash': 'awef',
            'is_active': True,
        },
    )


async def test(db_session, user):
    user = await UserRepository(db_session).get_by_username('asdf')

    assert user.username == 'asdf'


async def test_not_exist(db_session):
    with pytest.raises(UserNotFoundError):
        await UserRepository(db_session).get_by_username('not_exist_username')
