from typing import Optional

from asyncpg import Connection
from pydantic import BaseModel, parse_obj_as


class AyatModelShort(BaseModel):
    """Урезанная модель аята."""

    id: int
    mailing_day: Optional[int]


class Stringable(object):

    def __str__(self):
        raise NotImplementedError


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


def calculate_limit_offset_by_page_params(page_num, page_size):
    return (
        page_size,
        (page_num - 1) * page_size,
    )


class PaginatedSequenceQuery(Stringable):

    _base_query: Stringable
    _page_num: int
    _page_size: int

    def __init__(
        self,
        base_query: Stringable,
        page_num: int,
        page_size: int,
    ):
        self._base_query = base_query
        self._page_num = page_num
        self._page_size = page_size

    def __str__(self):
        limit, offset = calculate_limit_offset_by_page_params(self._page_num, self._page_size)
        return '{0}\n LIMIT {1} OFFSET {2}'.format(self._base_query, limit, offset)


class PaginatedSequence(object):

    _connection: Connection
    _query: Stringable
    _model_to_parse: type[BaseModel]

    def __init__(self, connection: Connection, query: Stringable, model_to_parse: type[BaseModel]):
        self._connection = connection
        self._query = query
        self._model_to_parse = model_to_parse

    async def get(self):
        rows = await self._connection.fetch(str(self._query))
        return parse_obj_as(list[self._model_to_parse], rows)


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


class PaginatedAyatResponse(BaseModel):
    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[AyatModelShort]


class PaginatedResponse(object):

    _page_num: int
    _page_size: int
    _elements_count: Count

    def __init__(
        self,
        page_num: int,
        page_size: int,
        elements_count: Count,
        elements: PaginatedSequence,
        url: str,
    ):
        self._page_num = page_num
        self._page_size = page_size
        self._elements_count = elements_count
        self._elements = elements
        self._url = url

    async def get(self):
        if self._page_num == 1:
            prev_page = None
        else:
            prev_page = '{0}?page_num={1}'.format(self._url, self._page_num - 1)
        elements_count = await self._elements_count.get()
        _, offset = calculate_limit_offset_by_page_params(self._page_num, self._page_size)
        if offset + self._page_size > elements_count:
            next_page = None
        else:
            next_page = '{0}?page_num={1}'.format(self._url, self._page_num + 1)

        return PaginatedAyatResponse(
            count=elements_count,
            next=next_page,
            prev=prev_page,
            results=await self._elements.get(),
        )