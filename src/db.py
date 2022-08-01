from typing import AsyncGenerator

from databases import Database

from settings import settings

connection_pool = None
database = Database(settings.DATABASE_URL)


async def db_connection() -> AsyncGenerator:
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    yield database
