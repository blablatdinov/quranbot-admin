from typing import AsyncGenerator

import asyncpg

from settings import settings

connection_pool = None


async def db_connection() -> AsyncGenerator:
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    global connection_pool  # noqa: WPS420 using for connection pool
    if connection_pool:
        async with connection_pool.acquire() as connection:
            yield connection
    else:
        pool = await asyncpg.create_pool(settings.DATABASE_URL)  # noqa: WPS442
        async with pool.acquire() as connection:  # type: ignore # noqa: WPS440
            yield connection
