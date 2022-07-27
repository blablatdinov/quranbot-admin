from asyncpg.connection import Connection
from fastapi import Depends
from pydantic import BaseModel
from pypika import Query, Table

from db import db_connection


class UserSchema(BaseModel):
    """Модель пользователя."""

    id: int
    username: str
    password: str


class UserRepositoryInterface(object):
    """Интерфейс для работы с хранилищем пользователей."""

    async def get_by_username(self, username: str):
        """Получить пользователя.

        :param username: str
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class UserRepository(UserRepositoryInterface):
    """Класс для работы с хранилищем пользователей."""

    _connection: Connection

    def __init__(self, connection: Connection = Depends(db_connection)):
        self._connection = connection

    async def get_by_username(self, username: str):
        """Получить пользователя.

        :param username: str
        :return: UserSchema
        """
        user_table = Table('auth_user')
        query = str(
            Query
            .select(user_table.id, user_table.username, user_table.password)
            .from_(user_table).where(user_table.username == username),
        )
        row = await self._connection.fetchrow(query)
        return UserSchema.parse_obj(row)
