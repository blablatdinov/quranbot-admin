import datetime
import uuid

from fastapi import Depends
from pydantic import BaseModel, parse_obj_as
from databases import Database

from db import db_connection
from handlers.v1.schemas.notifications import NotificationResponseSchema


class NotificationInsertQueryResult(BaseModel):

    uuid: uuid.UUID
    text: str


class NotificationRepositoryInterface(object):
    """Интерфейс репозитория для работы с хранилищем уведомлений."""

    async def create(self, text: str):
        """Создание уведомления.

        :param text: str
        """
        raise NotImplementedError

    async def mark_as_readed(self, notification_uuid):
        raise NotImplementedError

    async def get_notifications(self):
        raise NotImplementedError


class NotificationRepository(NotificationRepositoryInterface):

    def __init__(self, connection: Database = Depends(db_connection)):
        self._connection = connection

    async def create(self, text: str):
        query = """
            INSERT INTO notifications (uuid, text, created_at, is_readed)
            VALUES (:uuid, :text, :created_at, :is_readed)
            RETURNING (uuid, text)
        """
        row = await self._connection.execute(
            query,
            {
                'uuid': uuid.uuid4(),
                'text': text,
                'created_at': datetime.datetime.now(),
                'is_readed': False,
            },
        )
        return NotificationInsertQueryResult(uuid=row[0], text=row[1])

    async def mark_as_readed(self, notification_uuid):
        query = """
            UPDATE notifications
            SET is_readed = 't'
            WHERE uuid = :notification_uuid
        """
        await self._connection.execute(query, {'notification_uuid': notification_uuid})

    async def get_notifications(self):
        query = """
            SELECT uuid, text FROM notifications WHERE is_readed = 'f'
        """
        rows = await self._connection.fetch_all(query)
        return parse_obj_as(list[NotificationResponseSchema], rows)

