"""Последний день, на который есть контент.

Classes:
    LastContentDay
"""
from typing import final

import attrs
from databases import Database

from exceptions import AyatNotFoundError


@final
@attrs.define(frozen=True)
class LastContentDay(object):
    """Последний день, на который есть контент."""

    _pgsql: Database

    async def to_int(self) -> int:
        """Числовое представление.

        :return: int
        :raises AyatNotFoundError: if day not found
        """
        query = """
            SELECT day
            FROM ayats
            WHERE day IS NOT NULL
            ORDER BY day DESC
            LIMIT 1
        """
        row = await self._pgsql.fetch_one(query)
        if not row:
            raise AyatNotFoundError
        return int(row['day'])
