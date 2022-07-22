from typing import Literal

from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter(prefix='/daily-content')


class DailyContentInputModel(BaseModel):

    day_num: int
    ayat_ids: list[int]


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_daily_content(input_data: DailyContentInputModel):
    return


@router.get('/last-registered-day/', response_model=dict[Literal['day_num'], int])
def get_last_daily_content_day():
    return {'day_num': 1}
