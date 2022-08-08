"""Модуль, содержащий логику по обработке сокетов.

Classes:
    WebsocketUser
"""
import json

from fastapi import WebSocket
from loguru import logger
from quranbot_schema_registry import validate_schema

from repositories.auth import UserSchema


class WebsocketUser(object):
    """Класс, для отправки уведомлений в websocket."""

    def __init__(self, websocket: WebSocket, user: UserSchema):
        """Конструктор класса.

        :param websocket: WebSocket
        :param user: UserSchema
        """
        self._websocket = websocket
        self._user = user

    async def receive(self, event):
        """Обработчик событий.

        :param event: str
        """
        event_dict = json.loads(event.data.decode())
        event_log_data = 'event_id={0} event_name={1}'.format(event_dict['event_id'], event_dict['event_name'])
        if event_dict['event_name'] != 'Websocket.NotificationCreated':
            return
        try:
            validate_schema(event_dict, event_dict['event_name'], event_dict['event_version'])
        except TypeError as event_validate_error:
            logger.error('Validate {0} failed {1}'.format(event_log_data, str(event_validate_error)))
            return
        await self._websocket.send_text(
            json.dumps(
                {'uuid': event_dict['data']['uuid'], 'text': event_dict['data']['text']},
            ),
        )
        logger.info('Received websocket notification from nats, text: {0}. Event: {1}'.format(
            event_dict['data']['text'], event_dict,
        ))
