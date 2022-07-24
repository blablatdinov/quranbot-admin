class QueryInterface(object):
    """Интерфейс запроса в хранилище."""

    def query(self):
        """Получить запрос.

        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError
