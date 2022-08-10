"""Сервисный слой для работы с файлами.

Classes:
    DiskFile
    FileTriggeredToDownload
"""
from fastapi import Depends

from integrations.queue_integration import QueueIntegrationInterface
from repositories.file import FileRepository
from repositories.storage import FileSystemStorage


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

    async def save(self, filename, bytes_list):
        """Сохранить файл.

        :param filename: str
        :param bytes_list: bytes
        """
        self._path = await self._storage.write(filename, bytes_list)
        self._file_id = await self._file_repository.create(filename)

    def get_id(self):
        """Получить идентификатор.

        :return: int
        """
        return self._file_id

    def path(self):
        """Получить путь до файла.

        :return: int
        """
        return self._path

    def get_source(self):
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

    async def save(self, filename, bytes_list):
        """Сохранить файл.

        :param filename: str
        :param bytes_list: bytes
        """
        await self._origin.save(filename, bytes_list)
        await self._queue_integration.send(
            {
                'file_id': self._origin.get_id(),
                'source': self._origin.get_source(),
                'path': str(self._origin.path()),
            },
            'File.SendTriggered',
            1,
        )
