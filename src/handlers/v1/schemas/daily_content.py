"""Входные данные для определения дня ежедневного контента для аятов.

Classes:
    DailyContentInputModel
"""
from pydantic import BaseModel


class DailyContentInputModel(BaseModel):
    """Входные данные для определения дня ежедневного контента для аятов."""

    day_num: int
    ayat_ids: list[int]
