"""Модуль, отвечающий за работу с БД приложения.

В кач-ве постоянного хранилища приложения используется БД postgres
https://www.postgresql.org/

Functions:
    db_connection
"""
from typing import AsyncGenerator

from databases import Database

from settings import settings

database = Database(settings.DATABASE_URL)


async def db_connection() -> AsyncGenerator:
    """Зависимость для указания в контроллерах Fastapi.

    :yields: Connection
    """
    yield database
