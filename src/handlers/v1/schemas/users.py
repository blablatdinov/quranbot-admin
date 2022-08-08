"""Модуль схем данных пользователей.

Classes:
    ActionTypeEnum
"""
import enum


class ActionTypeEnum(str, enum.Enum):  # noqa: WPS600
    """Типы действий пользователей."""

    SUBSCRIBED = 'subscribed'
    UNSUBSCRIBED = 'unsubscribed'
    REACTIVATED = 'reactivated'
