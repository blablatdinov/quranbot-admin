from pypika.queries import QueryBuilder


class QueryInterface(object):
    """Интерфейс запроса в хранилище."""

    def query(self) -> QueryBuilder:
        """Получить запрос.

        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError
