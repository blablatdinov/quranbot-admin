"""Модуль, содержащий логику для работы с хранилищем файлов.

Classes:
    FilePaginatedQuery
    OrderedFileQuery
    FileRepositoryInterface
    FileRepository
"""
from databases import Database
from fastapi import Depends
from pypika import Order, Query, Table

from app_types.query import QueryInterface
from db.connection import db_connection
from services.limit_offset_by_page_params import LimitOffset


class FilePaginatedQuery(QueryInterface):
    """Запрос для просмотра файлов с пагинацией."""

    _files_table = Table('content_file')

    def __init__(self, limit_offset_calculator: LimitOffset):
        """Конструктор класса.

        :param limit_offset_calculator: LimitOffset
        """
        self._limit_offset_calculator = limit_offset_calculator

    def query(self):
        """Возвращает запрос.

        :return: str
        """
        limit, offset = self._limit_offset_calculator.calculate()
        return (
            Query()
            .from_(self._files_table)
            .select(
                self._files_table.id,
                self._files_table.tg_file_id.as_('telegram_file_id'),
                self._files_table.link_to_file.as_('link'),
                self._files_table.name,
            )
            .limit(limit)
            .offset(offset)
        )


class OrderedFileQuery(QueryInterface):
    """Отсортированный список файлов."""

    def __init__(self, origin_query: QueryInterface, order_param: str):
        """Конструктор класса.

        :param origin_query: QueryInterface
        :param order_param: str
        """
        self._origin = origin_query
        self._order_param = order_param

    def query(self):
        """Возвращает запрос.

        :return: pypika.QueryBuilder
        """
        if self._order_param.startswith('-'):
            return (
                self._origin.query()
                .orderby(self._order_param[1:], order=Order.asc)
            )

        return self._origin.query().orderby(self._order_param, order=Order.desc)


class FileRepositoryInterface(object):
    """Интерфейс для работы с хранилищем файлов."""

    async def create(self, filename: str):
        """Создать запись о файле.

        :param filename: str
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class FileRepository(FileRepositoryInterface):
    """Класс для работы с хранилищем файлов."""

    def __init__(self, connection: Database = Depends(db_connection)):
        """Конструктор класса.

        :param connection: Database
        """
        self._connection = connection

    async def create(self, filename: str):
        """Создать запись о файле.

        :param filename: str
        :return: int
        """
        query = 'INSERT INTO content_file (name) VALUES (:filename) RETURNING id'
        return await self._connection.execute(query, {'filename': filename})
