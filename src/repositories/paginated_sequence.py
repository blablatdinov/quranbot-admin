from asyncpg import Connection
from fastapi import Depends
from pydantic import BaseModel, parse_obj_as

from app_types.stringable import Stringable
from db import db_connection


class PaginatedSequenceInterface(object):

    def update_query(self, query: str) -> 'PaginatedSequenceInterface':
        raise NotImplementedError

    def update_model_to_parse(self, model_to_parse: type[BaseModel]):
        raise NotImplementedError

    async def get(self) -> list[BaseModel]:
        """Получить.

        :return: BaseModel
        """
        raise NotImplementedError


class PaginatedSequence(PaginatedSequenceInterface):
    """Класс, предоставляющий доступ к списку объектов с пагинацией."""

    _connection: Connection
    _query: Stringable
    _model_to_parse: type[BaseModel]

    def __init__(self, connection: Connection = Depends(db_connection)):
        self._connection = connection

    def update_query(self, query: str):
        new_instance = PaginatedSequence(
            self._connection,
        )
        new_instance.__dict__ = self.__dict__
        new_instance._query = query
        return new_instance

    def update_model_to_parse(self, model_to_parse: type[BaseModel]):
        new_instance = PaginatedSequence(
            self._connection,
        )
        new_instance.__dict__ = self.__dict__
        new_instance._model_to_parse = model_to_parse
        return new_instance

    async def get(self) -> list[BaseModel]:
        """Получить.

        :return: BaseModel
        """
        rows = await self._connection.fetch(str(self._query))
        return parse_obj_as(list[self._model_to_parse], rows)  # type: ignore
