"""Сервисный слой для работы с файлами.

Classes:
    DiskFile
    FileTriggeredToDownload
"""
import json
import time
import uuid
import datetime
from typing import final

import aioamqp
import aiofiles
import attrs
from databases import Database
from loguru import logger
from quranbot_schema_registry import validate_schema

from integrations.queue_integration import QueueIntegrationInterface
from settings import settings


@final
@attrs.define(frozen=True)
class PgFile(object):
    """Сервисный класс для создания файла на диске."""

    _file_id: uuid.UUID
    _pgsql: Database

    @classmethod
    async def new_file_ctor(cls, filename: str, file_bytes: bytes, pgsql: Database):
        async with aiofiles.open(settings.BASE_DIR / 'media' / filename, 'wb') as file_sink:
            await file_sink.write(file_bytes)
        query = """
            INSERT INTO files (file_id, created_at, filename)
            VALUES (:file_id, :created_at, :filename)
            RETURNING file_id
        """
        return cls(
            await pgsql.execute(query, {
                'file_id': str(uuid.uuid4()),
                'created_at': datetime.datetime.now(),
                'filename': filename,
            }),
            pgsql,
        )

    def file_id(self) -> uuid.UUID:
        """Получить идентификатор.

        :return: int
        """
        logger.info(f'Generated file id {self._file_id}')
        return self._file_id

    async def path(self) -> str:
        """Получить путь до файла.

        :return: int
        """
        return settings.BASE_DIR / 'media' / await self._pgsql.fetch_val(
            'SELECT filename FROM files WHERE file_id = :file_id',
            {'file_id': self._file_id}
        )

    def get_source(self) -> str:
        """Получить источник байтов.

        :return: int
        """
        return 'disk'


class FileToDownloadEvent(object):
    """Класс, чтобы создавать файлы и отправлять событие, чтобы другой сервис скачал и установил файлу file_id.

    https://core.telegram.org/bots/api#file
    """

    def __init__(self, file: PgFile):
        """Конструктор класса.

        :param file: DiskFile
        """
        self._origin = file

    async def trigger(self) -> None:
        """Сохранить файл.

        :param filename: str
        :param bytes_list: bytes
        """
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
            'event_name': 'File.SendTriggered',
            'event_time': str(int(time.time())),
            'producer': 'quranbot-admin',
            'data': {
                'file_id': self._origin.file_id(),
                'source': self._origin.get_source(),
                'path': str(await self._origin.path()),
            },
        }
        validate_schema(event_data, 'File.SendTriggered', 1)
        await channel.basic_publish(
            payload=json.dumps(event_data).encode('utf-8'),
            exchange_name='',
            routing_key='my_queue',
        )
        await channel.close()
        await protocol.close()
