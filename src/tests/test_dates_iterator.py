import datetime

from services.dates_iterator import DatesIterator


def test():
    got = list(DatesIterator(
        datetime.date(2020, 1, 1), datetime.date(2020, 2, 1),
    ))

    assert got == [
        datetime.date(2020, 1, 1) + datetime.timedelta(days=days_count)
        for days_count in range(31)
    ]
    assert got[0] == datetime.date(2020, 1, 1)
    assert got[-1] == datetime.date(2020, 1, 31)
    assert len(got) == 31
