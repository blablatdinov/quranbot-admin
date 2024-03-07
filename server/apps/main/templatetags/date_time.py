"""Фильтры для работы с датой/временем."""

import datetime

from django import template

register = template.Library()


@register.filter('timestamp_to_time')
def convert_timestamp_to_time(timestamp: float) -> datetime.datetime:
    """Конвертация timestamp в date."""
    return datetime.datetime.fromtimestamp(int(timestamp), tz=datetime.UTC)
