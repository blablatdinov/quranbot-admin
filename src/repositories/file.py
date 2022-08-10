"""Модуль, содержащий логику для работы с хранилищем файлов.

Classes:
    FilePaginatedQuery
    OrderedFileQuery
"""
from pypika import Order, Query, Table
from databases import Database
from fastapi import Depends

from app_types.query import QueryInterface
from services.limit_offset_by_page_params import LimitOffsetByPageParams
from db import db_connection


class FilePaginatedQuery(QueryInterface):
    """Запрос для просмотра файлов с пагинацией."""

    _files_table = Table('content_file')

    def __init__(self, limit_offset_calculator: LimitOffsetByPageParams):
        """Конструктор класса.

        :param limit_offset_calculator: LimitOffsetByPageParams
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

    async def create(self, filename: str):
        raise NotImplementedError


class FileRepository(FileRepositoryInterface):

    def __init__(self, connection: Database = Depends(db_connection)):
        self._connection = connection

    async def create(self, filename: str):
        query = """INSERT INTO content_file (name) VALUES (:filename) RETURNING id"""
        file_id = await self._connection.execute(query, {'filename': filename})
        return file_id
