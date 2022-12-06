"""Модуль, содержащий функцию для получения стартовой даты.

Functions:
    start_date_dependency
"""
import datetime

from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ErrorWrapper

from constants import FIRST_USER_ACTION_LOG_DATE
from exceptions import DateTimeError


def start_date_dependency(start_date: datetime.date | None = None):
    """Dependency для контроллеров fastapi, для определения стартовой даты.

    :param start_date: datetime.date
    :return: Optional[datetime.date]
    :raises RequestValidationError: if start_date invalid
    """
    if not start_date:
        return None
    if start_date < FIRST_USER_ACTION_LOG_DATE:
        raise RequestValidationError(errors=[
            ErrorWrapper(
                DateTimeError(limit_value=FIRST_USER_ACTION_LOG_DATE),
                loc=('query', 'start_date'),
            ),
        ])

    return start_date
