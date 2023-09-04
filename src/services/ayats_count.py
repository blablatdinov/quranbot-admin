"""Кол-во аятов.

Classes:
    AyatsCount
"""
from typing import final

import attrs
from databases import Database


@final
@attrs.define(frozen=True)
class AyatsCount(object):
    """Кол-во аятов."""

    _pgsql: Database

    async def to_int(self) -> int:
        """Числовое представление.

        :return: int
        """
        row = await self._pgsql.execute('SELECT COUNT(*) FROM ayats')
        return row['count']
