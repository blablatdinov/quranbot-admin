import asyncio

import pytest
from databases import Database
import asyncpg

from settings import settings


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(scope='session')
async def test_db(event_loop):
    origin_db = Database(settings.DATABASE_URL)
    await origin_db.connect()
    await origin_db.execute('DROP DATABASE IF EXISTS test_qbot')
    await origin_db.execute('CREATE DATABASE test_qbot')
    test_db_connection = await asyncpg.connect(settings.DATABASE_URL.replace('/qbot', '/test_qbot'))
    with open(settings.BASE_DIR / 'tests' / 'fixtures' / 'db_schema.sql') as f:
        await test_db_connection.execute(f.read())

    await test_db_connection.close()
    test_db = Database(settings.DATABASE_URL.replace('/qbot', '/test_qbot'))
    await test_db.connect()
    yield test_db
    await test_db.disconnect()
    await origin_db.execute('DROP DATABASE IF EXISTS test_qbot')
    await origin_db.disconnect()


@pytest.fixture()
async def db_session(test_db, event_loop):
    async with test_db.transaction(force_rollback=True):
        yield test_db
