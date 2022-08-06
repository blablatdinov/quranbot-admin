"""Модуль для работы с хранилищем сообщений.

Classes:
    MessagesCountQuery
    MessagesQuery
    FilteredMessageQuery
    PaginatedMessagesQuery
    MessagesSqlFilter
    ShortMessageQuery
"""
import datetime

from databases import Database
from fastapi import Depends
from pydantic import parse_obj_as
from pypika import Query as SqlQuery
from pypika import Table

from app_types.query import QueryInterface
from app_types.stringable import Stringable
from db import db_connection
from handlers.v1.schemas.messages import MessageGraphDataItem
from services.limit_offset_by_page_params import LimitOffsetByPageParams


class MessageRepositoryInterface(object):
    """Интерфейс для работы с хранилищем сообщений."""

    async def get_messages_for_graph(self, start_date: datetime.date, finish_date: datetime.date):
        """Получить данные для графика кол-ва сообщений.

        :param start_date: datetime.date
        :param finish_date: datetime.date
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class MessageRepository(MessageRepositoryInterface):
    """Класс для работы с хранилищем сообщений."""

    _connection: Database

    def __init__(self, connection: Database = Depends(db_connection)):
        """Конструктор класса.

        :param connection: Database
        """
        self._connection = connection

    async def get_messages_for_graph(
        self,
        start_date: datetime.date,
        finish_date: datetime.date,
    ) -> dict[datetime.date, int]:
        """Получить данные для графика кол-ва сообщений.

        :param start_date: datetime.date
        :param finish_date: datetime.date
        :return: dict[datetime.date, int]
        """
        query = """
            SELECT
                date::DATE,
                COUNT(*) AS messages_count
            FROM bot_init_message
            WHERE date BETWEEN :start_date AND :finish_date
            GROUP BY date::DATE
            ORDER BY date
        """
        rows = await self._connection.fetch_all(query, {'start_date': start_date, 'finish_date': finish_date})
        return {
            message_graph_data_item.date: message_graph_data_item.messages_count
            for message_graph_data_item in parse_obj_as(list[MessageGraphDataItem], rows)
        }


class MessagesCountQuery(Stringable):
    """Запрос для получению кол-ва сообщений."""

    _sql_query = 'SELECT COUNT(*) FROM bot_init_message m {filtering}'
    _sql_filter_param: Stringable

    def __init__(self, sql_filter_param: Stringable):
        """Конструктор класса.

        :param sql_filter_param: Stringable
        """
        self._sql_filter_param = sql_filter_param

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query.format(filtering=self._sql_filter_param)


class MessagesQuery(QueryInterface):
    """Запрос для получения сообщений."""

    _messages_table = Table('bot_init_message')

    def query(self) -> QueryInterface:
        """Получить запрос.

        :return: pypika.QueryBuilder
        """
        return (
            SqlQuery()
            .from_(self._messages_table)
            .select(
                self._messages_table.id,
                self._messages_table.from_user_id.as_('message_source'),
                self._messages_table.date.as_('sending_date'),
                self._messages_table.message_id,
                self._messages_table.text,
            )
            .orderby(self._messages_table.id)
        )


class FilteredMessageQuery(QueryInterface):
    """Запрос с фильтрацией."""

    _messages_table = Table('bot_init_message')

    def __init__(self, messages_query: QueryInterface, filter_param: str):
        """Конструктор класса.

        :param messages_query: QueryInterface
        :param filter_param: str
        """
        self._origin = messages_query
        self._filter_param = filter_param

    def query(self):
        """Получить запрос.

        :return: pypika.QueryBuilder
        """
        origin_query = self._origin.query()
        if self._filter_param == 'without_mailing':
            return origin_query.where(self._messages_table.mailing_id.isnull())
        elif self._filter_param == 'unknown':
            return origin_query.where(self._messages_table.is_unknown is True)
        return origin_query


class PaginatedMessagesQuery(QueryInterface):
    """Запрос с фильтрацией."""

    _messages_table = Table('bot_init_message')

    def __init__(self, messages_query: QueryInterface, limit_offset_calculator: LimitOffsetByPageParams):
        """Конструктор класса.

        :param messages_query: QueryInterface
        :param limit_offset_calculator: LimitOffsetByPageParams
        """
        self._origin = messages_query
        self._limit_offset_calculator = limit_offset_calculator

    def query(self):
        """Получить запрос.

        :return: pypika.QueryBuilder
        """
        limit, offset = self._limit_offset_calculator.calculate()
        return self._origin.query().limit(limit).offset(offset)
