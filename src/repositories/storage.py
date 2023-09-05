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
