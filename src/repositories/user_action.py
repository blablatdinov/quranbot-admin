"""Модуль, с функционалом для работы с данными о действиях пользователей.

Classes:
    QueryResult
    ActionCountMapQueryResult
    UserActionRepositoryInterface
    UserActionRepository
"""
import datetime

from databases import Database
from fastapi import Depends
from pydantic import BaseModel, parse_obj_as

from db import db_connection
from handlers.v1.schemas.users import ActionTypeEnum


class ActionsByDateRangeQueryResult(BaseModel):
    """Схема для парсинга результата о кол-ве действий в промежуток времени."""

    date: datetime.date
    action: ActionTypeEnum


class ActionCountMapQueryResult(BaseModel):
    """Схема для парсинга результата о кол-ве действий."""

    subscribed: int
    unsubscribed: int
    reactivated: int


class UserActionRepositoryInterface(object):
    """Интерфейс для работы с хранилищем действий пользователей."""

    async def get_action_count_map_until_date(self, date: datetime.date) -> ActionCountMapQueryResult:
        """Получить кол-во действий до переданной даты.

        :param date: datetime.date
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError

    async def get_user_actions_by_date_range(self, start_date: datetime.date, finish_date: datetime.date):
        """Получить действия пользователей в выбранный промежуток времени.

        :param start_date: datetime.date
        :param finish_date: datetime.date
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class UserActionRepository(UserActionRepositoryInterface):
    """Класс для работы с хранилищем действий пользователей."""

    def __init__(self, connection: Database = Depends(db_connection)):
        self._connection = connection

    async def get_action_count_map_until_date(self, date: datetime.date) -> ActionCountMapQueryResult:
        """Получить кол-во действий до переданной даты.

        :param date: datetime.date
        :return: ActionCountMapQueryResult
        """
        query = """
            SELECT
                action,
                count(id)
            FROM bot_init_subscriberaction bis
            WHERE date_time::DATE < :date
            GROUP BY action
        """
        rows = await self._connection.fetch_all(query, {'date': date})
        return ActionCountMapQueryResult(**{
            row._mapping['action']: row._mapping['count']  # noqa: WPS437
            for row in rows
        })

    async def get_user_actions_by_date_range(
        self,
        start_date: datetime.date,
        finish_date: datetime.date,
    ) -> list[ActionsByDateRangeQueryResult]:
        """Получить действия пользователей в выбранный промежуток времени.

        :param start_date: datetime.date
        :param finish_date: datetime.date
        :return: list[ActionsByDateRangeQueryResult]
        """
        query = """
            SELECT
                date_time::DATE AS date,
                action
            FROM bot_init_subscriberaction
            WHERE date_time::TIMESTAMP BETWEEN :start_date AND :finish_date
            ORDER BY date_time
        """
        rows = await self._connection.fetch_all(query, {'start_date': start_date, 'finish_date': finish_date})
        return parse_obj_as(list[ActionsByDateRangeQueryResult], rows)
