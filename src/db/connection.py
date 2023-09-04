"""Модуль, отвечающий за работу с БД приложения.

В кач-ве постоянного хранилища приложения используется БД postgres
https://www.postgresql.org/

Functions:
    db_connection
"""
from typing import AsyncGenerator

from databases import Database

from settings import settings


async def db_connection() -> AsyncGenerator:
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    async with Database(settings.DATABASE_URL) as database:
        yield database
