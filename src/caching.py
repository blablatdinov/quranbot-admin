"""Модуль, отвечающий за работу с "горячим" хранилищем.

Горячее хранилище используется в кач-ве кэша для исключения однотипных запросов к БД и по HTTP

В кач-ве средства для кеширования используется redis
https://redis.io/

Functions:
    redis_connection
"""
from redis.asyncio import Redis

from settings import settings


async def redis_connection() -> Redis:
    """Получить соеденение к redis.

    :return: Redis
    """
    return Redis(str(settings.REDIS_DSN))  # type: ignore
