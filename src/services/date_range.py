"""Модуль, с классом для Fastapi.Depends, который устанавливает стартовую и финальную дату.

Classes:
    DateRange
"""
import datetime


class DateRange(object):
    """Depend для использования start_date, finish_date в query параметрах."""

    def __init__(
        self,
        start_date: datetime.date | None = None,
        finish_date: datetime.date | None = None,
    ):
        """Конструктор класса.

        :param start_date: datetime.date
        :param finish_date: datetime.date
        """
        default_time_range_days = 30
        today = datetime.datetime.today()
        if not start_date:
            start_date = (today - datetime.timedelta(days=default_time_range_days)).date()
        if not finish_date:
            finish_date = today.date()
        self.start_date = start_date
        self.finish_date = finish_date
