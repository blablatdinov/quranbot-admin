from typing import AsyncGenerator

import asyncpg

from settings import settings


class QueriesCountConnection(asyncpg.Connection):
    """Обертка над asyncpg.Connection для подсчета кол-ва запросов."""

    def __init__(self, connection: asyncpg.Connection):
        self._connection = connection
        self._counter = 0

    @property
    def queries_count(self):
        """Возвращает кол-во сделанных запросов.

        :return: int
        """
        return self._counter

    async def execute(self, *args):
        """Прокси метода.

        :param args: tuple[Any]
        :return: Any
        """
        self._counter += 1
        return await self._connection.execute(*args)

    async def fetch(self, *args):
        """Прокси метода.

        :param args: tuple[Any]
        :return: Any
        """
        self._counter += 1
        return await self._connection.fetch(*args)

    async def fetchrow(self, *args):
        """Прокси метода.

        :param args: tuple[Any]
        :return: Any
        """
        self._counter += 1
        return await self._connection.fetchrow(*args)

    async def close(self, *args, **kwargs) -> None:
        """Прокси метода.

        :param args: tuple[Any]
        :param kwargs: dict[Any, Any]
        :return: Any
        """
        return await self._connection.close(*args, **kwargs)


async def db_connection() -> AsyncGenerator:
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    connection = await asyncpg.connect(settings.DATABASE_URL)
    yield connection
    await connection.close()
