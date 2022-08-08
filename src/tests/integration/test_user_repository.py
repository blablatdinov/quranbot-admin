import datetime

import pytest
from pypika import Parameter, Query, Table

from exceptions import UserNotFoundError
from repositories.auth import UserRepository


@pytest.fixture
async def user(db_session):
    user_table = Table('auth_user')
    columns = (
        'username',
        'password',
        'is_superuser',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
    )
    parameters = [Parameter(':{0}'.format(field)) for field in columns]
    await db_session.execute(
        query=str(
            Query()
            .into(user_table)
            .columns(*columns)
            .insert(*parameters),
        ),
        values={
            'username': 'asdf',
            'password': 'awef',
            'is_superuser': False,
            'first_name': 'guireoj',
            'last_name': 'eoirjg',
            'email': 'awef',
            'is_staff': False,
            'is_active': True,
            'date_joined': datetime.datetime(2020, 1, 1),
        },
    )


async def test(db_session, user):
    user = await UserRepository(db_session).get_by_username('asdf')

    assert user.username == 'asdf'


async def test_not_exist(db_session):
    with pytest.raises(UserNotFoundError):
        await UserRepository(db_session).get_by_username('not_exist_username')
