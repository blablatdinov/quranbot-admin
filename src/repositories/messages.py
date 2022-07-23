from typing import Literal

from app_types.stringable import Stringable


class MessagesCountQuery(Stringable):
    """Запрос для получению кол-ва сообщений."""

    _sql_query = 'SELECT COUNT(*) FROM bot_init_message m {filtering}'
    _sql_filter_param: Stringable

    def __init__(self, sql_filter_param: Stringable):
        self._sql_filter_param = sql_filter_param

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query.format(filtering=self._sql_filter_param)


class MessagesSqlFilter(Stringable):
    """Класс, собирающий параметр фильтрации."""

    _filter_param: Literal['without_mailing', 'unknown']

    def __init__(self, filter_param: Literal['without_mailing', 'unknown']):
        self._filter_param = filter_param

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        sql_filter_param = ''
        if self._filter_param == 'without_mailing':
            sql_filter_param = 'WHERE m.mailing_id IS NULL'
        elif self._filter_param == 'unknown':
            sql_filter_param = 'WHERE m.is_unknown = true'
        return sql_filter_param


class ShortMessageQuery(Stringable):
    """Запрос для получению урезанного списка сообщений."""

    _sql_query = """
        SELECT
            m.id,
            m.from_user_id AS message_source,
            m.date AS sending_date,
            m.message_id,
            m.text
        FROM bot_init_message m
        {filtering}
        ORDER BY m.id
    """
    _sql_filter_param: Stringable

    def __init__(self, sql_filter_param: Stringable):
        self._sql_filter_param = sql_filter_param

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query.format(filtering=self._sql_filter_param)
