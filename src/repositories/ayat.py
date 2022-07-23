from asyncpg import Connection
from fastapi import status, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

from app_types.stringable import Stringable
from db import db_connection
from handlers.v1.schemas.ayats import AyatModel, FileModel
from services.limit_offset_by_page_params import LimitOffsetByPageParams


class AyatDetailQuery(Stringable):
    """Запрос для получения детальной инфы по аяту."""

    _sql_query = """
            SELECT
                a.id,
                a.additional_content,
                a.ayat as ayat_num,
                a.arab_text,
                a.content,
                a.trans,
                a.audio_id,
                a.html,

                s.number as sura_num,
                s.link as sura_link,

                mc.day as mailing_day,

                cf.id as file_id,
                cf.tg_file_id as tg_file_id,
                cf.link_to_file as link,
                cf.name
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
    """Класс, представляющий аят."""

    _ayat: AyatModel

    def __init__(self, ayat: AyatModel):
        self._ayat = ayat

    def to_pydantic(self):
        """Преобразовать в pydantic объект.

        :return: AyatModel
        """
        return self._ayat

    @classmethod
    async def from_id(cls, connection: Connection, ayat_id: int, ayat_detail_query: Stringable):
        """Достать из БД по идентификатору.

        :param connection: Connection
        :param ayat_id: int
        :param ayat_detail_query: Stringable
        :return: Ayat
        :raises HTTPException: if not found
        """
        ayat_row = await connection.fetchrow(str(ayat_detail_query), ayat_id)
        if not ayat_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
        ayat_row = dict(ayat_row)
        file_model = FileModel(
            id=ayat_row.pop('file_id'),
            name=ayat_row.pop('name'),
            telegram_file_id=ayat_row.pop('tg_file_id'),
            link=ayat_row.pop('link'),
        )
        return cls(AyatModel(
            **ayat_row,
            audio_file=file_model,
        ))


class ElementsCountInterface(object):

    def update_query(self, query: str) -> 'ElementsCountInterface':
        raise NotImplementedError

    async def get(self) -> int:
        """Получить.

        :return: int
        """
        raise NotImplementedError


class ElementsCount(ElementsCountInterface):
    """Класс, осуществляющий запрос на кол-во в БД."""

    _connection: Connection
    _query: str

    def __init__(self, connection: Connection = Depends(db_connection)):
        self._connection = connection

    def update_query(self, query):
        new_instance = ElementsCount(self._connection)
        new_instance._query = query
        return new_instance

    async def get(self) -> int:
        """Получить.

        :return: int
        """
        row = await self._connection.fetchrow(self._query)
        return CountQueryResult.parse_obj(row).count
