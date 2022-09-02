"""Модуль для работы с данными аутентификации.

Classes:
    UserSchema
    UserRepositoryInterface
    UserRepository
"""
from typing import Optional

from databases import Database
from fastapi import Depends
from pydantic import BaseModel
from pypika import Query, Table

from db.connection import db_connection
from exceptions import UserNotFoundError


class UserSchema(BaseModel):
    """Модель пользователя."""

    id: int
    username: str
    password: str


class UserInsertSchema(BaseModel):
    """Модель пользователя."""

    chat_id: int
    day: int
    referrer_id: Optional[int]


class UserRepositoryInterface(object):
    """Интерфейс для работы с хранилищем пользователей."""

    async def get_by_username(self, username: str):
        """Получить пользователя.

        :param username: str
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError

    async def create(self, user: UserInsertSchema):
        """Создание пользователя.

        :param user: UserInsertSchema
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError

    async def update_status(self, chat_id: int, to: bool):
        """обновление статуса пользователя.

        :param chat_id: int
        :param to: bool
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class UserRepository(UserRepositoryInterface):
    """Класс для работы с хранилищем пользователей."""

    _connection: Database

    def __init__(self, connection: Database = Depends(db_connection)):
        """Конструктор класса.

        :param connection: Database
        """
        self._connection = connection

    async def get_by_username(self, username: str):
        """Получить пользователя.

        :param username: str
        :return: UserSchema
        :raises UserNotFoundError: если пользователь не найден
        """
        user_table = Table('users')
        query = str(
            Query
            .select(user_table.chat_id.as_('id'), user_table.username, user_table.password_hash.as_('password'))
            .from_(user_table).where(user_table.username == username),
        )
        row = await self._connection.fetch_one(query)
        if not row:
            raise UserNotFoundError
        # https://github.com/encode/databases/pull/447
        return UserSchema.parse_obj(row._mapping)  # noqa: WPS437

    async def create(self, user: UserInsertSchema):
        """Создание пользователя.

        :param user: UserInsertSchema
        """
        query = """
            INSERT INTO users
            (chat_id, is_active, day, referrer_id)
            VALUES
            (:chat_id, 't', :day, :referrer_id)
        """
        await self._connection.execute(query, user.dict())

    async def update_status(self, chat_id: int, to: bool):
        """обновление статуса пользователя.

        :param chat_id: int
        :param to: bool
        """
        query = """
            UPDATE users
            SET is_active = :is_active
            WHERE chat_id = :chat_id
        """
        await self._connection.execute(query, {'is_active': to, 'chat_id': chat_id})
