"""Сервисный слой для работы с файлами.

Classes:
    DiskFile
    FileTriggeredToDownload
"""
import json
import time
import uuid

import aioamqp
from fastapi import Depends
from quranbot_schema_registry import validate_schema

from integrations.queue_integration import QueueIntegrationInterface
from repositories.file import FileRepository
from repositories.storage import FileSystemStorage
from settings import settings


class DiskFile(object):
    """Сервисный класс для создания файла на диске."""

    def __init__(
        self,
        storage: FileSystemStorage = Depends(),
        file_repository: FileRepository = Depends(),
    ):
        """Конструктор класса.

        :param storage: FileSystemStorage
        :param file_repository: FileRepository
        """
        self._storage = storage
        self._file_repository = file_repository

    async def save(self, filename, bytes_list) -> None:
        """Сохранить файл.

        :param filename: str
        :param bytes_list: bytes
        """
        self._path = await self._storage.write(filename, bytes_list)
        self._file_id = await self._file_repository.create(filename)

    def get_id(self) -> int:
        """Получить идентификатор.

        :return: int
        """
        return self._file_id

    def path(self) -> str:
        """Получить путь до файла.

        :return: int
        """
        return self._path

    def get_source(self) -> str:
        """Получить источник байтов.

        :return: int
        """
        return 'disk'


class FileTriggeredToDownload(object):
    """Класс, чтобы создавать файлы и отправлять событие, чтобы другой сервис скачал и установил файлу file_id.

    https://core.telegram.org/bots/api#file
    """

    def __init__(self, file_service: DiskFile, queue_integration: QueueIntegrationInterface):
        """Конструктор класса.

        :param file_service: DiskFile
        :param queue_integration: QueueIntegrationInterface
        """
        self._origin = file_service
        self._queue_integration = queue_integration

    async def save(self, filename, bytes_list) -> None:
        """Сохранить файл.

        :param filename: str
        :param bytes_list: bytes
        """
        await self._origin.save(filename, bytes_list)

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
                'file_id': self._origin.get_id(),
                'source': self._origin.get_source(),
                'path': str(self._origin.path()),
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
