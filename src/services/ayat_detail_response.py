"""Детальный просмотр аята.

Classes:
    AyatDetailResponse
"""
from typing import final

import attrs
from databases import Database

from exceptions import AyatNotFoundError
from handlers.v1.schemas.ayats import AyatModel
from handlers.v1.schemas.files import FileModel


@final
@attrs.define
class AyatDetailResponse(object):
    """Детальный просмотр аята."""

    _pgsql: Database
    _ayat_id: int

    async def build(self) -> AyatModel:
        """Собрать ответ.

        :return: AyatModel
        :raises AyatNotFoundError: if ayat not found
        """
        query = """
            SELECT
                a.ayat_id,
                a.content,
                a.arab_text,
                a.transliteration,
                a.sura_id,
                a.ayat_number,
                a.audio_id,
                f.link,
                f.telegram_file_id
            FROM ayats AS a
            INNER JOIN files f ON a.audio_id = f.file_id
            WHERE a.ayat_id = :ayat_id
        """
        row = await self._pgsql.fetch_one(query, {'ayat_id': self._ayat_id})
        if not row:
            raise AyatNotFoundError
        return AyatModel(
            id=row['ayat_id'],
            additional_content='Not implemented',
            content=row['content'],
            arab_text=row['arab_text'],
            trans=row['transliteration'],
            sura_num=row['sura_id'],
            ayat_num=row['ayat_number'],
            html='Not implemented',
            audio_file=FileModel(
                id=row['audio_id'],
                link=row['link'],
                telegram_file_id=row['telegram_file_id'],
                name='Not implemented',
            ),
            mailing_day=0,  # TODO: not implemented
        )
