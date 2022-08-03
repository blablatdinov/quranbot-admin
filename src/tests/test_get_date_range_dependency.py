import datetime

from handlers.v1.views.users import _get_date_range


def test():
    start, finish = _get_date_range()

    assert type(start) == datetime.date
    assert type(finish) == datetime.date
