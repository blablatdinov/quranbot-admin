import asyncpg

from settings import settings


async def db_connection():
    connection = await asyncpg.connect(settings.DATABASE_URL)
    yield connection
    await connection.close()
