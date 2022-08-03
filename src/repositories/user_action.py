import datetime
import enum

from databases import Database
from fastapi import Depends
from pydantic import BaseModel, parse_obj_as

from db import db_connection


class ActionTypeEnum(str, enum.Enum):

    SUBSCRIBED = 'subscribed'
    UNSUBSCRIBED = 'unsubscribed'
    REACTIVATED = 'reactivated'
    DEACTIVATE = 'deactivate'  # deprecated


class QueryResult(BaseModel):

    date: datetime.date
    action: ActionTypeEnum


class ActionCountMapQueryResult(BaseModel):

    subscribed: int
    unsubscribed: int
    reactivated: int


class UserActionRepositoryInterface(object):

    async def get_action_count_map_until_date(self, date: datetime.date) -> ActionCountMapQueryResult:
        raise NotImplementedError

    async def get_user_actions_by_date_range(self, start_date: datetime.date, finish_date: datetime.date):
        raise NotImplementedError


class UserActionRepository(UserActionRepositoryInterface):

    def __init__(self, connection: Database = Depends(db_connection)):
        self._connection = connection

    async def get_action_count_map_until_date(self, date: datetime.date) -> ActionCountMapQueryResult:
        query = """
            SELECT
                action,
                count(id)
            FROM bot_init_subscriberaction bis
            WHERE date_time::DATE < :date
            GROUP BY action
        """
        rows = await self._connection.fetch_all(query, {'date': date})
        print({
            row._mapping['action']: row._mapping['count']
            for row in rows
        })
        return ActionCountMapQueryResult(**{
            row._mapping['action']: row._mapping['count']
            for row in rows
        })

    async def get_user_actions_by_date_range(
        self,
        start_date: datetime.date,
        finish_date: datetime.date,
    ) -> list[QueryResult]:
        query = """
            SELECT
                date_time::DATE AS date,
                action
            FROM bot_init_subscriberaction
            WHERE date_time::TIMESTAMP BETWEEN :start_date AND :finish_date
            ORDER BY date_time
        """
        rows = await self._connection.fetch_all(query, {'start_date': start_date, 'finish_date': finish_date})
        return parse_obj_as(list[QueryResult], rows)
