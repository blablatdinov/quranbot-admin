"""Обработчик websocket соединения.

Functions:
    websocket_endpoint
"""
import asyncio

import nats
from aioredis.client import Redis
from fastapi import Depends, Query, WebSocket

from caching import redis_connection
from services.auth import User
from services.websocket_user import WebsocketUser


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
    user = User.get_from_token(token)
    await websocket.accept()
    nats_client = await nats.connect('localhost')
    await redis.set('websocket_client_{0}'.format(user.username), 'true')
    await nats_client.subscribe('default', cb=WebsocketUser(websocket, user))
    while True:  # noqa: WPS457
        await asyncio.sleep(1)
