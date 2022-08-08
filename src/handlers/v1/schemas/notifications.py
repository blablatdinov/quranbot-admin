"""Модуль, хранящий схемы для уведомлений.

Classes:
    NotificationCreateModel
"""
import uuid

from pydantic import BaseModel


class NotificationCreateModel(BaseModel):
    """Модель для создания уведомлений."""

    text: str


class NotificationResponseSchema(BaseModel):

    uuid: uuid.UUID
    text: str
