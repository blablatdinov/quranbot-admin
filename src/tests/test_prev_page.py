from starlette.requests import URL

from repositories.ayat import ElementsCountInterface
from services.ayats import PrevPage


class ElementsCountMock(ElementsCountInterface):

    def __init__(self, input_value: int):
        self._input_value = input_value

    async def get(self):
        return self._input_value


async def test_for_first_page():
    got = await PrevPage(
        1,
        4,
        ElementsCountMock(50),
        URL('http://localhost'),
    ).calculate()

    assert got is None


async def test_for_middle_page():
    got = await PrevPage(
        5,
        1,
        ElementsCountMock(50),
        URL('http://localhost'),
    ).calculate()

    assert got is not None
    assert 'page_num=4' in got
    assert 'page_size=1' in got


async def test_for_out_of_scope_ayat():
    got = await PrevPage(
        7,
        1,
        ElementsCountMock(3),
        URL('http://localhost'),
    ).calculate()

    assert got is None


async def test_first_page_out_of_scope():
    got = await PrevPage(
        4,
        2,
        ElementsCountMock(8),
        URL('http://localhost'),
    ).calculate()

    assert got is not None
    assert 'page_num=3' in got
    assert 'page_size=2' in got
