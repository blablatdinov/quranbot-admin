import aiohttp


class ClientRequest(object):

    _url: str

    def __init__(self, url):
        self._url = url

    @classmethod
    def new(cls):
        return cls(url='')

    def url(self, url: str):
        return ClientRequest(url)

    async def act(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._url) as resp:
                text = await resp.text()

        return text


class HttpClient(object):

    def __init__(self, request: ClientRequest):
        self._request = request

    async def act(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._request.url) as resp:
                text = await resp.text()

        return text
