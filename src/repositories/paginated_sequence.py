
from asyncpg import Connection
from pydantic import BaseModel, parse_obj_as

from app_types.stringable import Stringable


class PaginatedSequence(object):
    """Класс, предоставляющий доступ к списку объектов с пагинацией."""

    _connection: Connection
    _query: Stringable
    _model_to_parse: type[BaseModel]

    def __init__(self, connection: Connection, query: Stringable, model_to_parse: type[BaseModel]):
        self._connection = connection
        self._query = query
        self._model_to_parse = model_to_parse

    async def get(self) -> list[BaseModel]:
        """Получить.

        :return: BaseModel
        """
        rows = await self._connection.fetch(str(self._query))
        return parse_obj_as(list[self._model_to_parse], rows)  # type: ignore
