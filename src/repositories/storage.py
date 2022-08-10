"""Модуль для работы с хранилищем файлов.

Classes:
    StorageInterface
    FileSystemStorage
"""
import aiofiles

from settings import settings


class StorageInterface(object):
    """Интерфейс хранилища."""

    async def write(self, filename: str, bytes_array: bytes):
        """Записать в хранилище.

        :param filename: str
        :param bytes_array: bytes
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class FileSystemStorage(StorageInterface):
    """Класс для записи файлов на диск."""

    async def write(self, filename: str, bytes_array: bytes):
        """Записать в хранилище.

        :param filename: str
        :param bytes_array: bytes
        :return: str
        """
        file_path = settings.BASE_DIR / 'media' / filename
        async with aiofiles.open(file_path, 'wb') as disk_file:
            await disk_file.write(bytes_array)

        return file_path
