from typing import AsyncGenerator

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from integrations.html_page import HtmlPage, HtmlPageInterface


class Ayat(BaseModel):
    sura_number: int
    ajat_caption: str
    arab_text: str = Field(..., alias='text_original')
    text_translate: str

    @property
    def ayat_number(self):
        return self.ajat_caption.split(':')[1]

    @property
    def content(self):
        return BeautifulSoup(self.text_translate, 'lxml').text.split('***')[0].strip()


class SuraData(BaseModel):

    ayats: list[Ayat] = Field(..., alias='ajats')


class PagePreloadData(BaseModel):
    sura_data: SuraData = Field(..., alias='suraData')


class UmmaRuState(BaseModel):
    page_preload_data: PagePreloadData = Field(..., alias='pagePreloadedData')

    @property
    def ayats(self):
        return self.page_preload_data.sura_data.ayats


class SuraLinksInterface(object):

    async def get_links(self) -> list[str]:
        raise NotImplementedError


class SuraPages(SuraLinksInterface):

    def __init__(self, html_page: HtmlPageInterface):
        self._html_page = html_page

    async def get_links(self):
        html = await self._html_page.read()
        soup = BeautifulSoup(html, 'lxml')
        item_list = soup.find('ol', class_="items-list")
        items = item_list.find_all('li')
        return [
            item.find('a')['href']
            for item in items
        ]


class FilteredSuraPages(SuraLinksInterface):

    def __init__(self, sura_pages: SuraLinksInterface):
        self._origin = sura_pages

    async def get_links(self) -> list[str]:
        return (await self._origin.get_links())[4:]


class AbsolutedSuraPages(SuraLinksInterface):

    def __init__(self, sura_pages: SuraLinksInterface):
        self._origin = sura_pages

    async def get_links(self):
        return [
            'https://umma.ru{0}'.format(link)
            for link in await self._origin.get_links()
        ]


class HtmlPagesFromLinks(object):

    def __init__(self, links: SuraLinksInterface):
        self._links = links

    async def pages(self) -> list[HtmlPageInterface]:
        return [
            HtmlPage(link)
            for link in await self._links.get_links()
        ]


class SuraPagesHTML(object):

    def __init__(self, html_pages: HtmlPagesFromLinks):
        self._html_pages = html_pages

    async def download(self):
        for sura_page in await self._html_pages.pages():
            yield sura_page


class Substring(object):

    async def find(self) -> AsyncGenerator:
        raise NotImplementedError


class PreloadedStateStrings(Substring):

    def __init__(self, sura_pages_html: SuraPagesHTML):
        self._sura_pages_html = sura_pages_html

    async def find(self) -> AsyncGenerator:
        sura_pages_generator = self._sura_pages_html.download()
        async for sura_page in sura_pages_generator:
            page = await sura_page.read()
            for line in page.split('\n'):
                if '__PRELOADED_STATE__' in line:
                    yield line


class TrimmedPreloadedStateString(Substring):

    def __init__(self, preloaded_state_string: Substring):
        self._preloaded_state_string = preloaded_state_string

    async def find(self) -> AsyncGenerator:
        async for preloaded_state_string in self._preloaded_state_string.find():
            yield preloaded_state_string[preloaded_state_string.find('{'):]


class ParsedPreloadedStateString(Substring):

    def __init__(self, preloaded_state_string: Substring):
        self._preloaded_state_string = preloaded_state_string

    async def find(self):
        async for preloaded_state_string in self._preloaded_state_string.find():
            yield UmmaRuState.parse_raw(preloaded_state_string)
