import asyncio

from integrations.client import ClientRequest
from integrations.umma import (
    AbsolutedSuraPages,
    FilteredSuraPages,
    RequestListFromUrls,
    SuraPages,
    SuraPagesHTML, PreloadedStateStrings, TrimmedPreloadedStateString,
)


class QuranParser(object):

    def __init__(self, data):
        self._data = data

    async def run(self):
        res = self._data.find()
        async for x in res:
            print(x)


class Main(object):

    def main(self):
        parser = QuranParser(
            TrimmedPreloadedStateString(
                PreloadedStateStrings(
                    SuraPagesHTML(
                        RequestListFromUrls(
                            AbsolutedSuraPages(
                                FilteredSuraPages(
                                    SuraPages(
                                        ClientRequest.new().url('https://umma.ru/perevod-korana/'),
                                    ),
                                ),
                            ),
                        )
                    )
                )
            )
        ).run()
        asyncio.run(parser)


if __name__ == '__main__':
    Main().main()
