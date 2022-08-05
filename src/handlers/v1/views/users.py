"""Обработчики HTTP запросов для просмотра данных о пользователях.

Functions:
    get_users_count_graph_data
    get_users_count
"""
import datetime

from fastapi import APIRouter, Depends
from pypika import Query as SqlQuery
from pypika.functions import Count

from constants import FIRST_USER_ACTION_LOG_DATE
from exceptions import DateTimeError
from handlers.v1.schemas.auth import UsersCountGithubBadge
from repositories.paginated_sequence import ElementsCount
from repositories.user_action import UserActionRepository
from services.auth import User
from services.date_range import DateRange
from services.user_count_graph_data import StartValue, UserCountGraphData
from services.start_date_dependency import start_date_dependency

router = APIRouter(prefix='/users')


@router.get('/graph-data/')
async def get_users_count_graph_data(
    user_action_repository: UserActionRepository = Depends(),
    start_date: datetime.date = Depends(start_date_dependency),
    finish_date: datetime.date = None,
    _: User = Depends(User.get_from_token),
):
    """Получить данные для графика по кол-ву пользователей.

    :param user_action_repository: UserActionRepository
    :param start_date: datetime.date
    :param finish_date: datetime.date
    :param _: User - param for checking authentification
    :return: dict
    """
    date_range = DateRange(start_date, finish_date)
    return await UserCountGraphData(
        user_action_repository,
        StartValue(
            user_action_repository,
            date_range.start_date,
        ),
    ).calculate(date_range.start_date, date_range.finish_date)


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
