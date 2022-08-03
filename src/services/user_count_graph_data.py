import datetime

from repositories.user_action import UserActionRepositoryInterface, ActionTypeEnum
from services.dates_iterator import DatesIterator


class StartValue(object):

    def __init__(self, user_action_repository, date: datetime.date):
        self._user_action_repository = user_action_repository
        self._date = date

    async def calculate(self):
        a = 0
        counts = await self._user_action_repository.get_action_count_map_until_date(self._date)
        start_value = a + counts.subscribed + counts.reactivated - counts.unsubscribed
        return start_value


class UserCountGraphData(object):

    def __init__(self, user_action_repository: UserActionRepositoryInterface, start_value: StartValue):
        self._user_repository = user_action_repository
        self._start_value = start_value

    async def calculate(self, start_date: datetime.date, finish_date: datetime.date):
        result = {}
        start_value = await self._start_value.calculate()
        objs = await self._user_repository.get_user_actions_by_date_range(start_date, finish_date)
        dates_iterator = DatesIterator(start_date, finish_date)
        for date in dates_iterator:
            result[date] = start_value
            date_objs = [obj for obj in objs if obj.date == date]
            for date_obj in date_objs:
                if date_obj.action in (ActionTypeEnum.SUBSCRIBED, ActionTypeEnum.REACTIVATED):
                    result[date] += 1
                elif date_obj.action == ActionTypeEnum.UNSUBSCRIBED:
                    result[date] -= 1

            start_value = result[date]
        return result
