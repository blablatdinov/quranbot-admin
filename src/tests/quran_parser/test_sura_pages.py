from pathlib import Path

import pytest

from integrations.html_page import HtmlPageInterface
from integrations.umma import FilteredSuraPages, SuraPages
from settings import settings


class HtmlPageMock(HtmlPageInterface):

    async def read(self):
        return Path(settings.BASE_DIR / 'src' / 'tests' / 'quran_parser' / 'fixtures' / 'perevod-korana.html').read_text()


@pytest.fixture()
def html_page_mock():
    return HtmlPageMock()


async def test(html_page_mock):
    got = await FilteredSuraPages(
        SuraPages(html_page_mock),
    ).get_links()

    assert len(got) == 114
    assert got[0] == 'https://umma.ru/sura-1-al-fatiha-otkryvayushhaya/'
    assert got[-1] == 'https://umma.ru/sura-114-an-nas-lyudi/'
