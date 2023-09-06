"""Обработчик websocket соединения.

Functions:
    websocket_endpoint
"""
import asyncio

from aioredis.client import Redis
from fastapi import Depends, Query, WebSocket

from caching import redis_connection


async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    redis: Redis = Depends(redis_connection),
):
    """Эндпоинт, обслуживающий websocket соединение.

    :param websocket: WebSocket
    :param token: str
    :param redis: Redis
    """
    await websocket.accept()
    while True:  # noqa: WPS457
        await asyncio.sleep(1)
