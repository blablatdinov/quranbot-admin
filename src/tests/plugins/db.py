import asyncio

import asyncpg
import pytest
from databases import Database

from settings import settings


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


async def _dump_test_db_schema() -> None:
    test_db_connection = await asyncpg.connect(settings.DATABASE_URL)
    await test_db_connection.close()


@pytest.fixture(scope='session')
async def test_db(event_loop):
    test_db = Database(settings.DATABASE_URL)
    await test_db.connect()
    yield test_db
    await test_db.disconnect()


@pytest.fixture()
async def db_session(test_db, event_loop):
    session = Database(settings.DATABASE_URL, force_rollback=True)
    await session.connect()
    yield session
    await session.disconnect()
