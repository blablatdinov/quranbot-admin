from asyncpg import Connection
from pydantic import BaseModel

from app_types.stringable import Stringable
from services.limit_offset_by_page_params import LimitOffsetByPageParams


class ShortAyatQuery(Stringable):
    """Запрос для получению урезанного списка аятов."""

    _sql_query = """
        SELECT
            a.id,
            cm.day AS mailing_day
        FROM content_ayat a
        LEFT JOIN content_morningcontent cm on a.one_day_content_id = cm.id
        ORDER BY a.id
    """

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query


class AyatCountQuery(Stringable):
    """Запрос для получению кол-ва аятов."""

    _sql_query = 'SELECT COUNT(*) FROM content_ayat'

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query


class CountQueryResult(BaseModel):
    """Модель для парсинга результата запроса о кол-ве элементов в БД."""

    count: int


class Count(object):
    """Класс, осуществляющий запрос на кол-во в БД."""

    _connection: Connection
    _query: Stringable

    def __init__(self, connection: Connection, query: Stringable):
        self._query = query
        self._connection = connection

    async def get(self) -> int:
        """Получить.

        :return: int
        """
        row = await self._connection.fetchrow(str(self._query))
        return CountQueryResult.parse_obj(row).count


class PaginatedSequenceQuery(Stringable):
    """Класс, трансформирующий запрос в запрос с пагинацией."""

    _base_query: Stringable
    _limit_offset_by_page_params: LimitOffsetByPageParams

    def __init__(
        self,
        base_query: Stringable,
        limit_offset_by_page_params: LimitOffsetByPageParams,
    ):
        self._base_query = base_query
        self._limit_offset_by_page_params = limit_offset_by_page_params

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        limit, offset = self._limit_offset_by_page_params.calculate()
        return '{0}\n LIMIT {1} OFFSET {2}'.format(self._base_query, limit, offset)
