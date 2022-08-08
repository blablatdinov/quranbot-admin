import datetime
import uuid

from fastapi import Depends
from pydantic import BaseModel
from databases import Database

from db import db_connection


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
