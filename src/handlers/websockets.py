import asyncio
import json

import nats
from aioredis.client import Redis
from fastapi import Depends, Query, Request, WebSocket
from loguru import logger
from pydantic import BaseModel
from quranbot_schema_registry import validate_schema

from caching import redis_connection
from repositories.auth import UserSchema
from services.auth import User


async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    redis: Redis = Depends(redis_connection),
):
    user = User.get_from_token(token)
    await websocket.accept()
    nats_client = await nats.connect('localhost')
    await redis.set('websocket_client_{0}'.format(user.username), 'true')

    async def _handle_message(event):
        event_dict = json.loads(event.data.decode())
        if event_dict['event_name'] != 'Websocket.NotificationCreated':
            return
        try:
            validate_schema(event_dict, event_dict['event_name'], event_dict['event_version'])
        except TypeError as event_validate_error:
            logger.error('Validate {0} failed {1}'.format(event_log_data, str(event_validate_error)))
            return
        await websocket.send_text(event_dict['data']['text'])
        logger.info('Received websocket notification from nats, text: {0}. Event: {1}'.format(
            event_dict['data']['text'], event_dict,
        ))

    sub = await nats_client.subscribe('default', cb=_handle_message)

    while True:
        await asyncio.sleep(1)
