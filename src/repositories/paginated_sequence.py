import json

from aioredis.client import Redis
from databases import Database
from fastapi import Depends
from loguru import logger
from pydantic import BaseModel, parse_obj_as, parse_raw_as

from app_types.query import QueryInterface
from caching import redis_connection
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

    _connection: Database
    _query: QueryInterface
    _model_to_parse: type[BaseModel]

    def __init__(self, connection: Database = Depends(db_connection)):
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

        :return: list[BaseModel]
        """
        rows = await self._connection.fetch_all(str(self._query))
        return parse_obj_as(list[self._model_to_parse], rows)  # type: ignore

    def __hash__(self):
        return hash(self._query)


class CachedPaginatedSequence(PaginatedSequenceInterface):
    """Класс для кеширования результата."""

    _origin: PaginatedSequenceInterface
    _cache_connection: Redis
    _model_to_parse: type[BaseModel]

    def __init__(
        self,
        redis: Redis = Depends(redis_connection),
        paginated_sequence: PaginatedSequenceInterface = Depends(PaginatedSequence),
    ):
        self._origin = paginated_sequence
        self._cache_connection = redis

    def update_query(self, query: QueryInterface):
        """Обновить запрос для хранилища.

        :param query: str
        :return: PaginatedSequenceInterface
        """
        origin = self._origin.update_query(query)
        return CachedPaginatedSequence(
            self._cache_connection,
            origin,
        )

    def update_model_to_parse(self, model_to_parse: type[BaseModel]):
        """ОБновить валидирующую модель.

        :param model_to_parse: type[BaseModel]
        :return: PaginatedSequenceInterface
        """
        origin = self._origin.update_model_to_parse(model_to_parse)
        new_instance = CachedPaginatedSequence(
            self._cache_connection,
            origin,
        )
        new_instance._model_to_parse = model_to_parse  # noqa: WPS437
        return new_instance

    async def get(self):
        """Получить.

        :return: list[BaseModel]
        """
        logger.info('Searching cached...')
        cache = await self._cache_connection.get(str(hash(self._origin)))
        if cache:
            logger.info('Cached data founded')
            return parse_raw_as(list[self._model_to_parse], cache)  # type: ignore

        logger.info('Cached data not founded')
        origin_get_result = await self._origin.get()
        logger.info('Setting data to cache')
        pagination_elements = [pagination_element.dict() for pagination_element in origin_get_result]
        await self._cache_connection.set(
            str(hash(self._origin)),
            json.dumps(pagination_elements),
            ex=60 * 60,
        )
        logger.info('Data setted to cache')
        return origin_get_result


class ElementsCountInterface(object):
    """Интерфейс для получение кол-ва элементов в хранилище."""

    def update_query(self, query: str) -> 'ElementsCountInterface':
        """Обновить запрос.

        :param query: str
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError

    async def get(self) -> int:
        """Получить.

        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class ElementsCount(ElementsCountInterface):
    """Класс, осуществляющий запрос на кол-во в БД."""

    _connection: Database
    _query: str

    def __init__(self, connection: Database = Depends(db_connection)):  # noqa: WPS404 Found complex default value
        self._connection = connection

    def update_query(self, query: str) -> 'ElementsCount':
        """Обновить запрос.

        :param query: str
        :return: ElementsCount
        """
        new_instance = ElementsCount(self._connection)
        new_instance._query = query  # noqa: WPS437 Found protected attribute usage
        return new_instance

    async def get(self) -> int:
        """Получить.

        :return: int
        """
        return await self._connection.fetch_val(self._query, column='count')
