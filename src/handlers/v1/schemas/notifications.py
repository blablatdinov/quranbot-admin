"""Модуль, хранящий схемы для уведомлений.

Classes:
    NotificationCreateModel
"""
from pydantic import BaseModel


class NotificationCreateModel(BaseModel):
    """Модель для создания уведомлений."""

    text: str
