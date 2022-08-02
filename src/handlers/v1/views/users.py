import datetime
from collections import namedtuple
import enum

from fastapi import APIRouter, Depends
from pydantic import BaseModel, parse_obj_as
from pypika import Query as SqlQuery
from pypika.functions import Count
from databases import Database

from db import db_connection
from handlers.v1.schemas.auth import UsersCountGithubBadge
from repositories.paginated_sequence import ElementsCount

router = APIRouter(prefix='/users')


def _get_date_range(start_date: datetime.date = None, finish_date: datetime.date = None):
    today = datetime.datetime.today()
    if not start_date:
        start_date = today - datetime.timedelta(days=30)
    if not finish_date:
        finish_date = today.date()
    return namedtuple('DateRange', 'start_date,finish_date')(
        start_date=start_date,
        finish_date=finish_date,
    )


def date_iterator(start_date, finish_date):
    while start_date < finish_date:
        yield start_date
        start_date += datetime.timedelta(days=1)


class ActionTypeEnum(str, enum.Enum):

    SUBSCRIBED = 'subscribed'
    UNSUBSCRIBED = 'unsubscribed'
    REACTIVATED = 'reactivated'
    DEACTIVATE = 'deactivate'


class QueryResult(BaseModel):

    date: datetime.date
    action: ActionTypeEnum


@router.get('/graph-data/')
async def get_users_count_graph_data(
    date_range: namedtuple = Depends(_get_date_range),
    connection: Database = Depends(db_connection),
):
    count_of_subscribed = await connection.fetch_val(
        "SELECT COUNT(*) FROM bot_init_subscriberaction WHERE date_time::DATE < :start_date AND action = 'subscribed'",
        {'start_date': date_range.start_date},
    )
    count_of_unsubscribed = await connection.fetch_val(
        "SELECT COUNT(*) FROM bot_init_subscriberaction WHERE date_time::DATE < :start_date AND action = 'unsubscribed'",
        {'start_date': date_range.start_date},
    )
    count_of_reactivated = await connection.fetch_val(
        "SELECT COUNT(*) FROM bot_init_subscriberaction WHERE date_time::DATE < :start_date AND action = 'reactivated'",
        {'start_date': date_range.start_date},
    )
    a = 1000
    start_value = a + count_of_subscribed + count_of_reactivated - count_of_unsubscribed
    print(f'{start_value=}')
    dates = [date.strftime('%Y-%m-%d') for date in date_iterator(date_range.start_date, date_range.finish_date)]
    query = """
        SELECT
            date_time::DATE AS date,
            action
        FROM bot_init_subscriberaction WHERE date_time::DATE IN {0}
        ORDER BY date_time
    """.format(str(tuple(dates)))
    result = {}
    rows = await connection.fetch_all(query)
    objs = parse_obj_as(list[QueryResult], rows)
    for date in date_iterator(date_range.start_date, date_range.finish_date):
        result[date] = start_value
        date_objs = list(filter(lambda obj: obj.date == date, objs))
        for date_obj in date_objs:
            if date_obj.action == ActionTypeEnum.SUBSCRIBED:
                result[date] += 1
            elif date_obj.action == ActionTypeEnum.UNSUBSCRIBED:
                result[date] -= 1
            elif date_obj.action == ActionTypeEnum.REACTIVATED:
                result[date] += 1

        start_value = result[date]
    return result


@router.get('/count-github-badge/')
async def get_users_count(elements_count: ElementsCount = Depends()) -> UsersCountGithubBadge:
    """Получить кол-во пользователей.

    :param elements_count: ElementsCount
    :return: UsersCountGithubBadge
    """
    count = elements_count.update_query(
        str(SqlQuery().from_('bot_init_subscriber').select(Count('*'))),
    )
    return UsersCountGithubBadge(
        label='users count',
        message=await count.get(),
    )
