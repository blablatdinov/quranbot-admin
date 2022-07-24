from asyncpg import Connection
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from pydantic.main import BaseModel
from pypika import Parameter
from pypika import Query as SqlQuery
from pypika import Table

from app_types.query import QueryInterface
from db import db_connection
from handlers.v1.schemas.ayats import AyatModel, FileModel
from services.limit_offset_by_page_params import LimitOffsetByPageParams


class AyatRepositoryInterface(object):
    """Интерфейс для работы с хранилищем аятов."""

    async def get_ayat_detail(self, ayat_id: int):
        """Получить данные для детального предстваления аята.

        :param ayat_id: int
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class AyatPaginatedQuery(QueryInterface):
    """Зпрос для получения списка аятов с пагинацией."""

    _ayats_table = Table('content_ayat')
    _morning_content_table = Table('content_morningcontent')
    _limit_offset_calculator: LimitOffsetByPageParams

    def __init__(self, limit_offset_calculator: LimitOffsetByPageParams):
        self._limit_offset_calculator = limit_offset_calculator

    def query(self):
        """Возвращает запрос.

        :return: str
        """
        limit, offset = self._limit_offset_calculator.calculate()
        select = (
            SqlQuery()
            .from_(self._ayats_table)
            .select(self._ayats_table.id, self._morning_content_table.day)
        )
        return str(
            select
            .left_join(self._morning_content_table)
            .on(self._ayats_table.one_day_content_id == self._morning_content_table.id)
            .orderby(self._ayats_table.id)
            .limit(limit)
            .offset(offset),
        )


class AyatDetailQuery(object):
    """Запрос для получения детального аята."""

    _ayat_table = Table('content_ayat')
    _sura_table = Table('content_sura')
    _morning_content_table = Table('content_morningcontent')
    _file_table = Table('content_file')

    def query(self):
        """Возвращает запрос.

        :return: str
        """
        select = (
            SqlQuery()
            .from_(self._ayat_table)
            .select(
                self._ayat_table.id,
                self._ayat_table.additional_content,
                self._ayat_table.ayat.as_('ayat_num'),
                self._ayat_table.arab_text,
                self._ayat_table.content,
                self._ayat_table.trans,
                self._ayat_table.html,
                self._sura_table.number.as_('sura_num'),
                self._sura_table.link,
                self._morning_content_table.day.as_('mailing_day'),
                self._file_table.id.as_('file_id'),
                self._file_table.tg_file_id.as_('tg_file_id'),
                self._file_table.link_to_file.as_('link'),
                self._file_table.name,
            )
        )
        joins = (
            select
            .inner_join(self._sura_table).on(self._ayat_table.sura_id == self._sura_table.id)
            .inner_join(self._morning_content_table)
            .on(self._ayat_table.one_day_content_id == self._morning_content_table.id)
            .inner_join(self._file_table).on(self._ayat_table.audio_id == self._file_table.id)
        )
        return str(
            joins
            .where(self._ayat_table.id == Parameter('$1')),
        )


class AyatRepository(AyatRepositoryInterface):
    """Класс для работы с хранилищем аятов."""

    _connection: Connection
    _ayat_detail_query: AyatDetailQuery

    def __init__(
        self,
        ayat_detail_query: AyatDetailQuery = Depends(),
        connection: Connection = Depends(db_connection),
    ):
        self._connection = connection
        self._ayat_detail_query = ayat_detail_query

    async def get_ayat_detail(self, ayat_id: int) -> AyatModel:
        """Получить данные для детального предстваления аята.

        :param ayat_id: int
        :return: AyatModel
        :raises HTTPException: if ayat not found
        """
        ayat_row = await self._connection.fetchrow(self._ayat_detail_query.query(), ayat_id)
        if not ayat_row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Item not found')
        ayat_row = dict(ayat_row)
        file_model = FileModel(
            id=ayat_row.pop('file_id'),
            name=ayat_row.pop('name'),
            telegram_file_id=ayat_row.pop('tg_file_id'),
            link=ayat_row.pop('link'),
        )
        return AyatModel(
            **ayat_row,
            audio_file=file_model,
        )


class ElementsCountInterface(object):
    """Интерфейс для получение кол-ва элементов в хранилище."""

    def update_query(self, query: str) -> 'ElementsCountInterface':
        """Обновить запрос.

        :param query: str
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError

    async def get(self) -> int:
        """Получить.

        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class CountQueryResult(BaseModel):
    """Модель для парсинга результата запроса о кол-ве элементов в БД."""

    count: int


class ElementsCount(ElementsCountInterface):
    """Класс, осуществляющий запрос на кол-во в БД."""

    _connection: Connection
    _query: str

    def __init__(self, connection: Connection = Depends(db_connection)):  # noqa: WPS404 Found complex default value
        self._connection = connection

    def update_query(self, query: str) -> 'ElementsCount':
        """Обновить запрос.

        :param query: str
        :return: ElementsCount
        """
        new_instance = ElementsCount(self._connection)
        new_instance._query = query  # noqa: WPS437 Found protected attribute usage
        return new_instance

    async def get(self) -> int:
        """Получить.

        :return: int
        """
        row = await self._connection.fetchrow(self._query)
        return CountQueryResult.parse_obj(row).count
