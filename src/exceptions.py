"""Модуль с исключениями.

Classes:
    DateTimeError
    UserNotFoundError
    IncorrectCredentialsError
"""
from http.client import HTTPException

from pydantic.errors import PydanticValueError


class DateTimeError(PydanticValueError):
    """Ошибка для отображения невалидной стартовой даты."""

    code = 'date.not_ge'
    msg_template = 'start date must be greater than 2020-07-09'


class UserNotFoundError(Exception):
    """Исключение, вызываемое если пользователь не найден."""

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return 'User not found'


class IncorrectCredentialsError(HTTPException):
    """Исключение, вызываемое при невалидных данных для доступа."""

    status_code = 400
