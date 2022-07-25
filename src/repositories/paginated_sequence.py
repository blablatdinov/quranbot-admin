from asyncpg import Connection
from fastapi import Depends
from pydantic import BaseModel, parse_obj_as

from app_types.query import QueryInterface
from db import db_connection


class PaginatedSequenceInterface(object):
    """Интерфейс для получения списка записей в хранилище."""

    def update_query(self, query: QueryInterface) -> 'PaginatedSequenceInterface':
        """Обновить запрос для хранилища.

        :param query: str
        :raises NotImplementedError: if not implement
        """
        raise NotImplementedError

    def update_model_to_parse(self, model_to_parse: type[BaseModel]):
        """ОБновить валидирующую модель.

        :param model_to_parse: type[BaseModel]
        :raises NotImplementedError: if not implement
        """
        raise NotImplementedError

    async def get(self) -> list[BaseModel]:
        """Получить.

        :raises NotImplementedError: if not implement
        """
        raise NotImplementedError


class PaginatedSequence(PaginatedSequenceInterface):
    """Класс, предоставляющий доступ к списку объектов с пагинацией."""

    _connection: Connection
    _query: QueryInterface
    _model_to_parse: type[BaseModel]

    def __init__(self, connection: Connection = Depends(db_connection)):
        self._connection = connection

    def update_query(self, query: QueryInterface):
        """Обновить запрос для хранилища.

        :param query: str
        :return: PaginatedSequenceInterface
        """
        new_instance = PaginatedSequence(
            self._connection,
        )
        new_instance.__dict__ = self.__dict__
        new_instance._query = query.query()  # noqa: WPS437 Found protected attribute usage: _query
        return new_instance

    def update_model_to_parse(self, model_to_parse: type[BaseModel]):
        """ОБновить валидирующую модель.

        :param model_to_parse: type[BaseModel]
        :return: PaginatedSequenceInterface
        """
        new_instance = PaginatedSequence(
            self._connection,
        )
        new_instance.__dict__ = self.__dict__
        new_instance._model_to_parse = model_to_parse  # noqa: WPS437 Found protected attribute usage: _query
        return new_instance

    async def get(self) -> list[BaseModel]:
        """Получить.

        :return: BaseModel
        """
        rows = await self._connection.fetch(str(self._query))
        return parse_obj_as(list[self._model_to_parse], rows)  # type: ignore
