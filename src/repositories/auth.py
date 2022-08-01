from fastapi import Depends
from pydantic import BaseModel
from pypika import Query, Table
from databases import Database

from db import db_connection
from exceptions import UserNotFoundError


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

    _connection: Database

    def __init__(self, connection: Database = Depends(db_connection)):
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
        row = await self._connection.fetch_one(query)
        if not row:
            raise UserNotFoundError
        return UserSchema.parse_obj(row._mapping)
