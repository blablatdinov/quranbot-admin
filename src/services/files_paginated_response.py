"""HTTP ответ со списком аятов.

Classes:
    AyatsPaginatedResponse
"""
from typing import final

import attrs
from databases import Database

from handlers.v1.schemas.ayats import PaginatedAyatResponse
from handlers.v1.schemas.files import PaginatedFileResponse
from services.ayats_count import AyatsCount
from services.pg_ayats_list import PgAyatsList
from services.pg_files_list import PgFilesList


@final
@attrs.define(frozen=True)
class FilesCount(object):

    _pgsql: Database

    async def to_int(self) -> int:
        return await self._pgsql.fetch_val('SELECT COUNT(*) FROM files')


@final
@attrs.define(frozen=True)
class FilesPaginatedResponse(object):
    """HTTP ответ со списком файлов."""

    _count: FilesCount
    _files_list: PgFilesList

    async def build(self) -> PaginatedFileResponse:
        """Сборка ответа.

        :return: PaginatedAyatResponse
        """
        return PaginatedFileResponse(
            count=1,
            prev=None,
            next=2,
            results=await self._files_list.models(),
        )
