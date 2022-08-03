import datetime


class DatesIterator(object):

    def __init__(self, start_date: datetime.date, finish_date: datetime.date):
        self._start_date = start_date
        self._finish_date = finish_date

    def __iter__(self):
        return self

    def __next__(self):
        value = self._start_date
        if value >= self._finish_date:
            raise StopIteration
        self._start_date += datetime.timedelta(days=1)
        return value
