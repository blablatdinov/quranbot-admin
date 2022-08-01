import asyncio
from pathlib import Path

import asyncpg
import pytest
from databases import Database
from fastapi.testclient import TestClient

from main import app
from settings import settings

test_db_dsn = settings.DATABASE_URL.replace('/qbot', '/test_qbot')


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


async def _create_test_db() -> None:
    origin_db = Database(settings.DATABASE_URL)
    await origin_db.connect()
    await origin_db.execute('CREATE DATABASE test_qbot')
    await origin_db.disconnect()


async def _dump_test_db_schema() -> None:
    test_db_connection = await asyncpg.connect(test_db_dsn)
    db_schema_file = Path(settings.BASE_DIR / 'tests' / 'fixtures' / 'db_schema.sql').read_text()
    await test_db_connection.execute(db_schema_file)

    await test_db_connection.close()


async def _remove_test_db() -> None:
    origin_db = Database(settings.DATABASE_URL)
    await origin_db.connect()
    await origin_db.execute('DROP DATABASE IF EXISTS test_qbot')
    await origin_db.disconnect()


@pytest.fixture(scope='session')
async def test_db(event_loop):
    await _create_test_db()
    await _dump_test_db_schema()
    test_db = Database(test_db_dsn)
    await test_db.connect()
    yield test_db
    await test_db.disconnect()
    await _remove_test_db()


@pytest.fixture()
async def db_session(test_db, event_loop):
    async with test_db.transaction(force_rollback=True):
        yield test_db


@pytest.fixture()
def client():
    http_client = TestClient(app)
    http_client.headers = {'Authorization': ''}
    return http_client
