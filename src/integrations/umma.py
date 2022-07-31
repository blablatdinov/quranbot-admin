import json

import aiohttp
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from integrations.client import ClientRequest


class Ayat(BaseModel):
    sura_number: str
    ajat_caption: str
    text_original: str
    text_translate: str


class SuraData(BaseModel):

    ayats: list[Ayat] = Field(..., alias='ajats')


class PagePreloadData(BaseModel):
    sura_data: SuraData = Field(..., alias='suraData')


class UmmaRuState(BaseModel):
    page_preload_data: PagePreloadData = Field(..., alias='pagePreloadedData')


class SuraPagesInterface(object):

    async def get_links(self):
        raise NotImplementedError


class SuraPages(SuraPagesInterface):

    def __init__(self, http_client):
        self._http_client = http_client

    async def get_links(self):
        html = await self._http_client.act()
        soup = BeautifulSoup(html, 'lxml')
        item_list = soup.find('ol', class_="items-list")
        items = item_list.find_all('li')
        return [
            item.find('a')['href']
            for item in items
        ]


class FilteredSuraPages(SuraPagesInterface):

    def __init__(self, sura_pages: SuraPagesInterface):
        self._origin = sura_pages

    async def get_links(self):
        return (await self._origin.get_links())[4:]


class AbsolutedSuraPages(SuraPagesInterface):

    def __init__(self, sura_pages: SuraPagesInterface):
        self._origin = sura_pages

    async def get_links(self):
        return [
            'https://umma.ru{0}'.format(link)
            for link in await self._origin.get_links()
        ]


class SuraPagesIterator(object):

    def __init__(self, sura_pages: SuraPagesInterface, sura_parser):
        self._sura_pages = sura_pages
        self._sura_parser = sura_parser

    async def run(self):
        sura_links = await self._sura_pages.get_links()
        for sura_link in sura_links:
            await self._sura_parser.parse(ClientRequest.new().url(sura_link))
            break


class SuraScriptTagParser(object):

    async def parse(self, soup: BeautifulSoup):
        pass


class RequestListFromUrls(object):

    def __init__(self, sura_pages_links: AbsolutedSuraPages):
        self._sura_pages_links = sura_pages_links

    async def transform(self) -> list[ClientRequest]:
        return [
            ClientRequest.new().url(link)
            for link in await self._sura_pages_links.get_links()
        ]


class SuraPagesHTML(object):

    def __init__(self, request_list: RequestListFromUrls):
        self._request_list = request_list

    async def download(self):
        for request in await self._request_list.transform():
            yield await request.act()


class JsonStrings():


class PreloadedStateStrings(object):

    def __init__(self, sura_pages_html: SuraPagesHTML):
        self._sura_pages_html = sura_pages_html

    async def find(self):
        sura_pages_generator = self._sura_pages_html.download()
        async for sura_page in sura_pages_generator:
            for line in sura_page.split('\n'):
                if '__PRELOADED_STATE__' in line:
                    yield line


class TrimmedPreloadedStateString(object):

    def __init__(self, preloaded_state_string: PreloadedStateStrings):
        self._preloaded_state_string = preloaded_state_string

    async def find(self):
        async for preloaded_state_string in self._preloaded_state_string.find():
            yield UmmaRuState.parse_raw(preloaded_state_string[preloaded_state_string.find('{'):])


class TrimmedPreloadedStateString(object):
