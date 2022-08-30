"""Модуль, содержащий логику работы с хранилищем уведомлений.

Classes:
    NotificationInsertQueryResult
    NotificationRepositoryInterface
    NotificationRepository
"""
import datetime
import uuid

from databases import Database
from fastapi import Depends
from pydantic import BaseModel, parse_obj_as

from db.connection import db_connection
from handlers.v1.schemas.notifications import NotificationResponseSchema


class NotificationInsertQueryResult(BaseModel):
    """Схема результата создания уведомления."""

    uuid: uuid.UUID
    text: str


class NotificationRepositoryInterface(object):
    """Интерфейс репозитория для работы с хранилищем уведомлений."""

    async def create(self, notification_uuid: uuid.UUID, text: str):
        """Создание уведомления.

        :param text: str
        :param notification_uuid: uuid.UUID
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError

    async def mark_as_readed(self, notification_uuid):
        """Пометить уведомление прочитанным.

        :param notification_uuid: uuid.UUID
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError

    async def get_notifications(self):
        """Получить список уведомлений.

        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class NotificationRepository(NotificationRepositoryInterface):
    """Класс для работы с хранилищем уведомлений."""

    def __init__(self, connection: Database = Depends(db_connection)):
        """Конструктор класса.

        :param connection: Database
        """
        self._connection = connection

    async def create(self, notification_uuid: uuid.UUID, text: str):
        """Создание уведомления.

        :param notification_uuid: uuid.UUID
        :param text: str
        :return: NotificationInsertQueryResult
        """
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

    async def mark_as_readed(self, notification_uuid) -> None:
        """Пометить уведомление прочитанным.

        :param notification_uuid: uuid.UUID
        """
        query = """
            UPDATE notifications
            SET is_readed = 't'
            WHERE uuid = :notification_uuid
        """
        await self._connection.execute(query, {'notification_uuid': notification_uuid})

    async def get_notifications(self) -> list[NotificationResponseSchema]:
        """Получить список уведомлений.

        :return: list[NotificationResponseSchema]
        """
        query = """
            SELECT uuid, text FROM notifications WHERE is_readed = 'f'
        """
        rows = await self._connection.fetch_all(query)
        return parse_obj_as(list[NotificationResponseSchema], rows)
