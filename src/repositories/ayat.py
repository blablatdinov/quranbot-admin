from asyncpg import Connection
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from pypika import Parameter
from pypika import Query as SqlQuery
from pypika import Table

from db import db_connection
from handlers.v1.schemas.ayats import AyatModel, FileModel


class AyatRepositoryInterface(object):

    async def get_ayat_detail(self, ayat_id: int):
        raise NotImplementedError


class AyatRepository(AyatRepositoryInterface):

    _connection: Connection

    def __init__(self, connection: Connection = Depends(db_connection)):
        self._connection = connection

    async def get_ayat_detail(self, ayat_id: int):
        ayat_table = Table('content_ayat')
        sura_table = Table('content_sura')
        morning_content_table = Table('content_morningcontent')
        file_table = Table('content_file')
        query = str(
            SqlQuery()
            .from_(ayat_table)
            .select(
                ayat_table.id,
                ayat_table.additional_content,
                ayat_table.ayat.as_('ayat_num'),
                ayat_table.arab_text,
                ayat_table.content,
                ayat_table.trans,
                ayat_table.html,
                sura_table.number.as_('sura_num'),
                sura_table.link,
                morning_content_table.day.as_('mailing_day'),
                file_table.id.as_('file_id'),
                file_table.tg_file_id.as_('tg_file_id'),
                file_table.link_to_file.as_('link'),
                file_table.name,
            )
            .inner_join(sura_table).on(ayat_table.sura_id == sura_table.id)
            .inner_join(morning_content_table).on(ayat_table.one_day_content_id == morning_content_table.id)
            .inner_join(file_table).on(ayat_table.audio_id == file_table.id)
            .where(ayat_table.id == Parameter('$1'))
        )
        ayat_row = await self._connection.fetchrow(query, ayat_id)
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
