"""Создание ежедневного контента.

Classes:
    NewDailyContent
"""
import json
import time
import uuid
from typing import final

import aioamqp
import attrs
from databases import Database
from quranbot_schema_registry import validate_schema

from handlers.v1.schemas.daily_content import DailyContentInputModel
from settings import settings


@final
@attrs.define(frozen=True)
class NewDailyContent(object):
    """Создание ежедневного контента."""

    _pgsql: Database
    _input_data: DailyContentInputModel

    async def create(self) -> None:
        """Создание."""
        query = """
            UPDATE ayats
            SET day = :day
            WHERE ayat_id = ANY(:ayat_ids)
        """
        await self._pgsql.execute(
            query,
            {'day': self._input_data.day_num, 'ayat_ids': self._input_data.ayat_ids},
        )
        await self._publish_event()

    async def _publish_event(self) -> None:
        transport, protocol = await aioamqp.connect(
            host=settings.RABBITMQ_HOST,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASS,
        )
        channel = await protocol.channel()
        event_data = {
            'event_id': str(uuid.uuid4()),
            'event_version': 1,
            'event_name': 'DailyContent.Created',
            'event_time': str(int(time.time())),
            'producer': 'quranbot-admin',
            'data': {
                'day': self._input_data.day_num,
                'ayat_ids': self._input_data.ayat_ids,
            },
        }
        validate_schema(event_data, 'DailyContent.Created', 1)
        await channel.basic_publish(
            payload=json.dumps(event_data).encode('utf-8'),
            exchange_name='',
            routing_key='my_queue',
        )
        await channel.close()
        await protocol.close()
