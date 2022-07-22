from typing import Optional

from pydantic import BaseModel

from app_types.stringable import Stringable
from handlers.v1.schemas.ayats import AyatModelShort
from repositories.ayat import Count
from repositories.paginated_sequence import PaginatedSequence


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


class PaginatedAyatResponse(BaseModel):
    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[AyatModelShort]


class PaginatedResponse(object):

    _page_num: int
    _page_size: int
    _elements_count: Count
    _elements: PaginatedSequence
    _url: str
    _response_model: type[BaseModel]

    def __init__(
        self,
        page_num: int,
        page_size: int,
        elements_count: Count,
        elements: PaginatedSequence,
        url: str,
        response_model: type[BaseModel],
    ):
        self._page_num = page_num
        self._page_size = page_size
        self._elements_count = elements_count
        self._elements = elements
        self._url = url
        self._response_model = response_model

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

        return self._response_model(
            count=elements_count,
            next=next_page,
            prev=prev_page,
            results=await self._elements.get(),
        )
