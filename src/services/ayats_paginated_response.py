from typing import final
import attrs

from handlers.v1.schemas.ayats import PaginatedAyatResponse
from services.ayats_count import AyatsCount
from services.pg_ayats_list import PgAyatsList


@final
@attrs.define(frozen=True)
class AyatsPaginatedResponse:

    _count: AyatsCount
    _ayats_list: PgAyatsList

    async def build(self):
        return PaginatedAyatResponse(
            count=1,
            prev=None,
            next=2,
            results=await self._ayats_list.models(),
        )
