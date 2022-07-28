import asyncio

from integrations.client import HttpClient
from integrations.umma import SuraPages, FilteredSuraPages, SuraPagesInterface, AbsolutedSuraPages


class QuranParser(object):

    def __init__(self, sura_links: SuraPagesInterface):
        self._sura_links = sura_links

    async def run(self):
        links = await self._sura_links.get_links()
        print(links)


class Main(object):

    def main(self):
        parser = QuranParser(
            AbsolutedSuraPages(
                FilteredSuraPages(
                    SuraPages(
                        HttpClient('https://umma.ru/perevod-korana/'),
                    ),
                ),
            )
        ).run()
        asyncio.run(parser)


if __name__ == '__main__':
    Main().main()
