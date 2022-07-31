from typing import AsyncGenerator

import asyncpg

from settings import settings
from databases import Database

connection_pool = None
database = Database(settings.DATABASE_URL)


async def db_connection() -> AsyncGenerator:
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    yield database
    # global connection_pool  # noqa: WPS420 using for connection pool
    # if connection_pool:
    #     async with connection_pool.acquire() as connection:
    #         yield connection
    # else:
    #     pool = await asyncpg.create_pool(settings.DATABASE_URL)  # noqa: WPS442
    #     async with pool.acquire() as connection:  # type: ignore # noqa: WPS440
    #         yield connection
