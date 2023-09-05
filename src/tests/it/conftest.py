import json
import time

import pika
import pytest
from databases import Database

from main import startup
from settings import settings
from tests.it.creating_test_db import create_db, drop_db, fill_test_db


@pytest.fixture(scope='session')
def migrate():
    create_db()
    fill_test_db()
    yield
    drop_db()


@pytest.fixture()
async def pgsql(migrate):
    await startup()
    database = Database(settings.DATABASE_URL)
    await database.connect()
    yield database
    await database.disconnect()


@pytest.fixture()
def wait_event(migrate):
    def _wait_event(name, version):
        for _ in range(50):
            published_event = json.loads(
                pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host='localhost',
                        port=5672,
                        credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASS),
                    ),
                )
                .channel()
                .basic_get(queue='my_queue', auto_ack=True)[2]
                .decode('utf-8'),
            )
            time.sleep(0.1)
            if published_event['event_name'] == name and published_event['event_version'] == version:
                return published_event
        raise TimeoutError
    return _wait_event
