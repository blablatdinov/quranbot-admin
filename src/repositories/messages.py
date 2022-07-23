from app_types.stringable import Stringable


class MessagesCountQuery(Stringable):
    """Запрос для получению кол-ва сообщений."""

    _sql_query = 'SELECT COUNT(*) FROM bot_init_message'

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query


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
        ORDER BY m.id
    """

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query
