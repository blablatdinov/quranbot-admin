"""Модуль для работы с хранилищем сообщений.

Classes:
    MessagesCountQuery
    MessagesQuery
    FilteredMessageQuery
    PaginatedMessagesQuery
    MessagesSqlFilter
    ShortMessageQuery
"""
from typing import Literal

from pypika import Query as SqlQuery
from pypika import Table

from app_types.query import QueryInterface
from app_types.stringable import Stringable
from services.limit_offset_by_page_params import LimitOffsetByPageParams


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
