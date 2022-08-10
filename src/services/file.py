from fastapi import Depends

from repositories.storage import FileSystemStorage
from repositories.file import FileRepository
from integrations.queue_integration import QueueIntegrationInterface


class DiskFile(object):

    def __init__(
        self,
        storage: FileSystemStorage = Depends(),
        file_repository: FileRepository = Depends(),
    ):
        self._storage = storage
        self._file_repository = file_repository

    async def save(self, filename, bytes_list):
        self._path = await self._storage.write(filename, bytes_list)
        self._file_id = await self._file_repository.create(filename)

    def get_id(self):
        return self._file_id

    def get_path(self):
        return self._path


class FileTriggeredToDownload(object):

    def __init__(self, file: DiskFile, queue_integration: QueueIntegrationInterface):
        self._origin = file
        self._queue_integration = queue_integration

    async def save(self, filename, bytes_list):
        await self._origin.save(filename, bytes_list)
        await self._queue_integration.send(
            {'file_id': self._origin.get_id(), 'source': 'disk', 'path': str(self._origin.get_path())},
            'File.SendTriggered',
            1,
        )
