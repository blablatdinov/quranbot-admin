"""Модуль с обработчиками HTTP запросов для работы с ежедневным контентом.

Functions:
    create_daily_content
    get_last_daily_content_day

Misc variables:
    router
"""
from typing import Literal

from databases import Database
from fastapi import APIRouter, Depends, status

from db.connection import db_connection
from handlers.v1.schemas.daily_content import DailyContentInputModel
from services.last_content_day import LastContentDay
from services.new_daily_content import NewDailyContent

router = APIRouter(prefix='/daily-content')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_daily_content(
    input_data: DailyContentInputModel,
    pgsql: Database = Depends(db_connection),
):
    """Определить день ежедневного контента для аятов.

    :param input_data: DailyContentInputModel
    :param pgsql: Database
    """
    await NewDailyContent(pgsql, input_data).create()


@router.get('/last-registered-day/', response_model=dict[Literal['day_num'], int])
async def get_last_daily_content_day(
    pgsql: Database = Depends(db_connection),
) -> dict[Literal['day_num'], int]:
    """Получить номер последнего дня, на который есть ежедневный контент.

    :param pgsql: Database
    :return: dict[Literal['day_num'], int]
    """
    return {'day_num': await LastContentDay(pgsql).to_int()}
