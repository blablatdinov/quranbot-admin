import datetime
from collections import namedtuple

from fastapi import APIRouter, Depends
from pypika import Query as SqlQuery
from pypika.functions import Count

from handlers.v1.schemas.auth import UsersCountGithubBadge
from repositories.paginated_sequence import ElementsCount

router = APIRouter(prefix='/users')


def _get_date_range(start_date: datetime.date = None, finish_date: datetime.date = None):
    today = datetime.datetime.today()
    if not start_date:
        start_date = today - datetime.timedelta(days=30)
    if not finish_date:
        finish_date = today
    return namedtuple('DateRange', 'start_date,finish_date')(
        start_date=start_date,
        finish_date=finish_date,
    )


@router.get('/graph-data/')
async def get_users_count_graph_data(
    date_range: namedtuple = Depends(_get_date_range)
):
    return {'start_date': date_range.start_date, 'finish_date': date_range.finish_date}


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
