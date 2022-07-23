from asyncpg import Connection
from pydantic import BaseModel

from app_types.stringable import Stringable
from handlers.v1.schemas.ayats import AyatModel, File
from services.limit_offset_by_page_params import LimitOffsetByPageParams


class ShortAyatQuery(Stringable):
    """Запрос для получению урезанного списка аятов."""

    _sql_query = """
        SELECT
            a.id,
            cm.day AS mailing_day
        FROM content_ayat a
        LEFT JOIN content_morningcontent cm ON a.one_day_content_id = cm.id
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


class AyatDetailQuery(Stringable):

    _sql_query = """
            SELECT
                a.id,
                a.additional_content,
                s.number as sura_num,
                s.link as sura_link,
                a.ayat as ayat_num,
                a.arab_text,
                a.content,
                a.trans,
                a.audio_id,
                a.html,
                mc.day as mailing_day,
                cf.tg_file_id as tg_file_id,
                cf.link_to_file as link,
                cf.name,
                cf.id as file_id
            FROM content_ayat a
            INNER JOIN content_sura s on a.sura_id = s.id
            INNER JOIN content_morningcontent mc on mc.id = a.one_day_content_id
            INNER JOIN content_file cf on a.audio_id = cf.id
            WHERE a.id = $1
    """

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return self._sql_query


class CountQueryResult(BaseModel):
    """Модель для парсинга результата запроса о кол-ве элементов в БД."""

    count: int


class Ayat(object):

    _ayat: AyatModel

    def __init__(self, ayat: AyatModel):
        self._ayat = ayat

    def to_pydantic(self):
        return self._ayat

    @classmethod
    async def from_id(cls, connection: Connection, id: int, ayat_detail_query: Stringable):
        ayat_row = await connection.fetchrow(str(ayat_detail_query), id)
        ayat_row = dict(ayat_row)
        file = File(
            id=ayat_row.pop('file_id'),
            name=ayat_row.pop('name'),
            telegram_file_id=ayat_row.pop('tg_file_id'),
            link=ayat_row.pop('link'),
        )
        return cls(AyatModel(
            **ayat_row,
            audio_file=file,
        ))


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
