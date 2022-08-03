import datetime

from services.date_range import DateRange


def test():
    got = DateRange()

    assert isinstance(got.start_date, datetime.date)
    assert isinstance(got.finish_date, datetime.date)
