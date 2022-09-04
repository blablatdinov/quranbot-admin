import time

import aiohttp
from loguru import logger


class HtmlPageInterface(object):

    async def read(self):
        raise NotImplementedError


class LoggedHtmlPage(HtmlPageInterface):

    def __init__(self, html_page: HtmlPageInterface):
        self._origin = html_page

    async def read(self):
        logger.info('Try read {0}'.format(self._origin))
        start_time = time.time()
        content = await self._origin.read()
        logger.info('{0} readed by {1} s'.format(self._origin, start_time - time.time()))
        return content


class HtmlPage(HtmlPageInterface):

    def __init__(self, url: str):
        self._url = url

    def __str__(self):
        return 'HtmlPage ({0})'.format(self._url)

    async def read(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as resp:
                return await resp.text()
