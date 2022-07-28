import aiohttp

from bs4 import BeautifulSoup


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
