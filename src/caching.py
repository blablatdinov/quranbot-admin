from settings import settings
import aioredis


async def redis_connection():
    return await aioredis.from_url(str(settings.REDIS_DSN))
