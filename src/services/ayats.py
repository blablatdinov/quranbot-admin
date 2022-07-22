from typing import Optional, TypeVar

from pydantic import BaseModel

from repositories.ayat import Count
from repositories.paginated_sequence import PaginatedSequence
from services.limit_offset_by_page_params import LimitOffsetByPageParams

PydanticModel = TypeVar('PydanticModel', bound=BaseModel)


class NextPage(object):
    """Класс умеющий расчитывать ссылку на след. страницу."""

    _page_num: int
    _page_size: int
    _url: str
    _elements_count: Count
    _limit_offset_by_page_params: LimitOffsetByPageParams

    def __init__(  # noqa: WPS211
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

    async def calculate(self) -> Optional[str]:
        """Расчет.

        :return: str
        """
        elements_count = await self._elements_count.get()
        _, offset = self._limit_offset_by_page_params.calculate()
        if offset + self._page_size > elements_count:
            return None
        return '{0}?page_num={1}'.format(self._url, self._page_num + 1)


class PrevPage(object):
    """Класс умеющий расчитывать ссылку на пред. страницу."""

    _page_num: int
    _url: str

    def __init__(self, page_num: int, url: str):
        self._page_num = page_num
        self._url = url

    async def calculate(self) -> Optional[str]:
        """Расчет.

        :return: str
        """
        if self._page_num == 1:
            return None
        return '{0}?page_num={1}'.format(self._url, self._page_num - 1)


class NeighborsPageLinks(object):
    """Ссылки на соседние страницы."""

    _prev_page: PrevPage
    _next_page: NextPage

    def __init__(self, prev_page: PrevPage, next_page: NextPage):
        self._prev_page = prev_page
        self._next_page = next_page

    async def calculate(self) -> tuple[Optional[str], Optional[str]]:
        """Расчет.

        :return: tuple[str, str]
        """
        return (
            await self._prev_page.calculate(),
            await self._next_page.calculate(),
        )


class PaginatedResponse(object):
    """Класс, представляющий ответ с пагинацией."""

    _elements_count: Count
    _elements: PaginatedSequence
    _response_model: type[PydanticModel]  # type: ignore
    _neighbors_page_links: NeighborsPageLinks

    def __init__(
        self,
        elements_count: Count,
        elements: PaginatedSequence,
        response_model: type[PydanticModel],
        neighbors_page_links: NeighborsPageLinks,
    ):
        self._elements_count = elements_count
        self._elements = elements
        self._response_model = response_model
        self._neighbors_page_links = neighbors_page_links

    async def get(self) -> PydanticModel:
        """Получить.

        :return: BaseModel
        """
        prev_page, next_page = await self._neighbors_page_links.calculate()
        print(await self._elements.get())
        print(self._response_model)
        return self._response_model(  # type: ignore
            count=await self._elements_count.get(),
            next=next_page,
            prev=prev_page,
            results=await self._elements.get(),
        )
