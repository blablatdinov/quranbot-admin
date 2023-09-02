import psycopg2
import pytest
from databases import Database

from settings import settings
from tests.integration.creating_test_db import create_db, drop_db, fill_test_db


@pytest.fixture(scope='session')
def migrate():
    create_db()
    fill_test_db()
    yield
    drop_db()


@pytest.fixture()
async def pgsql(migrate):
    database = Database(settings.DATABASE_URL)
    await database.connect()
    yield database
    await database.disconnect()
