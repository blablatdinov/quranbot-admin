from asyncpg.connection import Connection
from pydantic import BaseModel
from fastapi import Depends

from pypika import Table, Query

from db import db_connection


class UserSchema(BaseModel):

    id: int
    username: str
    password: str


class UserRepositoryInterface(object):

    async def get_by_username(self, username: str):
        raise NotImplementedError


class UserRepository(UserRepositoryInterface):

    _connection: Connection

    def __init__(self, connection: Connection = Depends(db_connection)):
        self._connection = connection

    async def get_by_username(self, username: str):
        user_table = Table('auth_user')
        query = str(
            Query
            .select(user_table.id, user_table.username, user_table.password)
            .from_(user_table).where(user_table.username == username)
        )
        row = await self._connection.fetchrow(query)
        return UserSchema.parse_obj(row)
