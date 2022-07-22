from typing import Optional

from pydantic import BaseModel

from handlers.v1.schemas.ayats import AyatModelShort
from repositories.ayat import Count
from repositories.paginated_sequence import PaginatedSequence
from services.limit_offset_by_page_params import LimitOffsetByPageParams


class PaginatedAyatResponse(BaseModel):
    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[AyatModelShort]


class NextPage(object):

    _page_num: int
    _page_size: int
    _url: str
    _elements_count: Count
    _limit_offset_by_page_params: LimitOffsetByPageParams

    def __init__(
        self,
        page_num: int,
        page_size: int,
        url: str,
        elements_count: Count,
        limit_offset_by_page_params: LimitOffsetByPageParams,
    ):
        self._page_num = page_num
        self._page_size = page_size
        self._url = url
        self._elements_count = elements_count
        self._limit_offset_by_page_params = limit_offset_by_page_params

    async def calculate(self):
        elements_count = await self._elements_count.get()
        _, offset = self._limit_offset_by_page_params.calculate()
        if offset + self._page_size > elements_count:
            return None
        return '{0}?page_num={1}'.format(self._url, self._page_num + 1)


class PrevPage(object):

    _page_num: int
    _url: str

    def __init__(self, page_num: int, url: str):
        self._page_num = page_num
        self._url = url

    async def calculate(self):
        if self._page_num == 1:
            return None
        return '{0}?page_num={1}'.format(self._url, self._page_num - 1)


class PaginatedResponse(object):

    _elements_count: Count
    _elements: PaginatedSequence
    _response_model: type[BaseModel]
    _prev_page: PrevPage
    _next_page: NextPage

    def __init__(
        self,
        elements_count: Count,
        elements: PaginatedSequence,
        response_model: type[BaseModel],
        prev_page: PrevPage,
        next_page: NextPage,
    ):
        self._elements_count = elements_count
        self._elements = elements
        self._response_model = response_model
        self._prev_page = prev_page
        self._next_page = next_page

    async def get(self):
        return self._response_model(
            count=await self._elements_count.get(),
            next=await self._next_page.calculate(),
            prev=await self._prev_page.calculate(),
            results=await self._elements.get(),
        )
