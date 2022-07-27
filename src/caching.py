import aioredis

from settings import settings


async def redis_connection():
    """Получить соеденение к redis.

    :return: Redis
    """
    return await aioredis.from_url(str(settings.REDIS_DSN))  # type: ignore
