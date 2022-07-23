from typing import AsyncGenerator

import asyncpg

from settings import settings


class QueriesCountConnection(asyncpg.Connection):

    def __init__(self, connection: asyncpg.Connection):
        self._connection = connection
        self._counter = 0

    @property
    def queries_count(self):
        return self._counter

    async def execute(self, *args):
        self._counter += 1
        return await self._connection.execute(*args)

    async def fetch(self, *args):
        self._counter += 1
        return await self._connection.fetch(*args)

    async def fetchrow(self, *args):
        self._counter += 1
        return await self._connection.fetchrow(*args)

    async def close(self, *args, **kwargs) -> None:
        return await self._connection.close(*args, **kwargs)


async def db_connection() -> AsyncGenerator:
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    connection = await asyncpg.connect(settings.DATABASE_URL)
    yield connection
    await connection.close()
