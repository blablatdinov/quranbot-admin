import asyncpg
import pytest
from fastapi.testclient import TestClient

from db import db_connection
from main import app
from settings import settings


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
async def create_db():  # noqa: WPS217
    base_connection = await asyncpg.connect(settings.DATABASE_URL)
    await base_connection.execute('DROP DATABASE IF EXISTS qbot_test')
    await base_connection.execute('CREATE DATABASE qbot_test')
    connection = await asyncpg.connect(settings.DATABASE_URL.replace('qbot', 'qbot_test'))
    with open(settings.BASE_DIR / 'tests/fixtures/db_schema.sql', 'r') as sql_schema_file:
        await connection.execute(sql_schema_file.read())
        yield connection

    await connection.close()
    await base_connection.execute('DROP DATABASE qbot_test')
    await base_connection.close()


async def override_db_connection():
    try:  # noqa: WPS501, WPS229
        connection = await asyncpg.connect(settings.DATABASE_URL.replace('qbot', 'qbot_test'))
        yield connection
    finally:
        await connection.close()


@pytest.fixture()
def db(create_db):
    app.dependency_overrides[db_connection] = override_db_connection


@pytest.fixture()
async def test_db_connection(create_db):
    connection = await asyncpg.connect(settings.DATABASE_URL.replace('qbot', 'qbot_test'))
    yield connection
    await connection.close()
