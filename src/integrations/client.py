import aiohttp


class HttpClient(object):

    def __init__(self, url):
        self._url = url

    async def act(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as resp:
                text = await resp.text()

        return text
