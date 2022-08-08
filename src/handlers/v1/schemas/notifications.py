"""Модуль, хранящий схемы для уведомлений.

Classes:
    NotificationCreateModel
    NotificationResponseSchema
"""
import uuid

from pydantic import BaseModel


class NotificationCreateModel(BaseModel):
    """Модель для создания уведомлений."""

    text: str


class NotificationResponseSchema(BaseModel):
    """Схема ответа для просмотра уведомлений."""

    uuid: uuid.UUID
    text: str
