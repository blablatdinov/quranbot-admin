import asyncpg

from settings import settings


async def db_connection():
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    connection = await asyncpg.connect(settings.DATABASE_URL)
    yield connection
    await connection.close()
