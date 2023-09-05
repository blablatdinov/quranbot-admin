"""Список аятов.

Classes:
    PgFilesList
"""
from typing import final

import attrs
from databases import Database

from handlers.v1.schemas.files import FileModel
from services.limit_offset_by_page_params import LimitOffset


@final
@attrs.define(frozen=True)
class PgFilesList(object):
    """Список аятов."""

    _pgsql: Database
    _limit_offset: LimitOffset

    async def models(self) -> list[FileModel]:
        """Модели.

        :return: list[AyatModelShort]
        """
        query = """
            SELECT
                file_id,
                link,
                telegram_file_id
            FROM files AS a
            ORDER BY file_id
            LIMIT :limit
            OFFSET :offset
        """
        rows = await self._pgsql.fetch_all(query, {
            'limit': self._limit_offset.limit(),
            'offset': self._limit_offset.offset(),
        })
        return [
            FileModel(
                id=row['file_id'],
                link=row['link'],
                telegram_file_id=row['telegram_file_id'],
                name='Not implemented',
            )
            for row in rows
        ]
