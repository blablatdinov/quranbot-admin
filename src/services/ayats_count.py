from typing import final

import attrs
from databases import Database


@final
@attrs.define(frozen=True)
class AyatsCount:

    _pgsql: Database

    async def to_int(self) -> int:
        row = await self._pgsql.execute('SELECT COUNT(*) FROM ayats')
        return row['count']
