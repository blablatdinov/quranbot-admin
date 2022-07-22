from asyncpg import Connection
from pydantic import BaseModel, parse_obj_as

from app_types.stringable import Stringable


class ShortAyatQuery(Stringable):

    _value = """
        SELECT 
            a.id,
            cm.day AS mailing_day
        FROM content_ayat a
        LEFT JOIN content_morningcontent cm on a.one_day_content_id = cm.id
        ORDER BY a.id
    """

    def __str__(self):
        return self._value


class AyatCountQuery(Stringable):

    _value = 'SELECT COUNT(*) FROM content_ayat'

    def __str__(self):
        return self._value


class CountQueryResult(BaseModel):

    count: int


class Count(object):

    _connection: Connection
    _query: Stringable

    def __init__(self, connection: Connection, query: Stringable):
        self._query = query
        self._connection = connection

    async def get(self):
        row = await self._connection.fetchrow(str(self._query))
        return CountQueryResult.parse_obj(row).count
