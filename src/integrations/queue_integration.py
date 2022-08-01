"""Интеграция с шиной сообщений.

В кач-ве шины сообщений используется https://nats.io/
Для валидации сообщений, отправляемых в шину и поддержки совместимости используется собственное решение,
основанное на https://json-schema.org/
Репозиторий схем событий - https://github.com/blablatdinov/quranbot-schema-registry

Classes:
    QueueIntegrationInterface
    NatsIntegration
"""
import datetime
import json
import uuid

import nats
from quranbot_schema_registry import validate_schema


class QueueIntegrationInterface(object):
    """Интерфейс интеграции с шиной событий."""

    async def send(self, event: dict, event_name: str, version: int):
        """Отправить событие.

        :param event: dict
        :param event_name: str
        :param version: int
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class NatsIntegration(QueueIntegrationInterface):
    """Интеграция с nats."""

    async def send(self, event_data, event_name, version):
        """Отправить событие.

        :param event_data: dict
        :param event_name: str
        :param version: int
        """
        event = {
            'event_id': str(uuid.uuid4()),
            'event_version': version,
            'event_name': event_name,
            'event_time': str(datetime.datetime.now()),
            'producer': 'quranbot-admin',
            'data': event_data,
        }
        validate_schema(event, event_name, version)
        nats_client = await nats.connect('localhost')
        await nats_client.publish('foo', json.dumps(event).encode('utf-8'))
        await nats_client.close()
