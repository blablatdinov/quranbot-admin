import aiofiles

from settings import settings


class StorageInterface(object):

    async def write(self, filename: str, bytes_array: bytes):
        raise NotImplementedError


class FileTelegramFileId(object):
    pass


class FileSystemStorage(StorageInterface):

    async def write(self, filename: str, bytes_array: bytes):
        file_path = settings.BASE_DIR / 'media' / filename
        async with aiofiles.open(file_path, 'wb') as disk_file:
            await disk_file.write(bytes_array)

        return file_path
