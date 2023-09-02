from typing import final

import attrs
from databases import Database
from pydantic import parse_obj_as

from handlers.v1.schemas.ayats import AyatModelShort
from services.limit_offset_by_page_params import LimitOffset


@final
@attrs.define(frozen=True)
class PgAyatsList:

    _pgsql: Database
    _limit_offset: LimitOffset

    async def models(self) -> list[AyatModelShort]:
        query = """
            SELECT
                ayat_id AS id,
                content,
                arab_text,
                transliteration AS trans,
                sura_id AS sura_num,
                ayat_number AS ayat_num,
                f.link AS audio_file_link
            FROM ayats AS a
            INNER JOIN files AS f ON a.audio_id = f.file_id
            ORDER BY ayat_id
            LIMIT :limit
            OFFSET :offset
        """
        rows = await self._pgsql.fetch_all(query, {
            'limit': self._limit_offset.limit(),
            'offset': self._limit_offset.offset(),
        })
        ayats = []
        for row in rows:
            ayats.append(AyatModelShort(
                id=row['id'],
                content=row['content'],
                arab_text=row['arab_text'],
                trans=row['trans'],
                sura_num=row['sura_num'],
                ayat_num=row['ayat_num'],
                audio_file_link=row['audio_file_link'],
            ))
        return ayats
