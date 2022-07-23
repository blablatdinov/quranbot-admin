from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix='/daily-content')


class DailyContentInputModel(BaseModel):
    """Входные данные для определения дня ежедневного контента для аятов."""

    day_num: int
    ayat_ids: list[int]


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_daily_content(input_data: DailyContentInputModel):
    """Определить день ежедневного контента для аятов.

    :param input_data: DailyContentInputModel
    """
    return  # noqa: WPS324


@router.get('/last-registered-day/', response_model=dict[Literal['day_num'], int])
def get_last_daily_content_day() -> dict[Literal['day_num'], int]:
    """Получить номер последнего дня, на который есть ежедневный контент.

    :return: dict[Literal['day_num'], int]
    """
    return {'day_num': 1}
