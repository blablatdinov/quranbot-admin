"""Сервисный слой для составления графиков пользователей.

Classes:
    StartValue
    UserCountGraphData
"""
import datetime

from repositories.user_action import ActionTypeEnum, UserActionRepositoryInterface
from services.dates_iterator import DatesIterator


class StartValue(object):
    """Класс, расчитывающий начальное значение для графика."""

    def __init__(self, user_action_repository, date: datetime.date):
        self._user_action_repository = user_action_repository
        self._date = date

    async def calculate(self) -> int:
        """Расчет.

        :return: int
        """
        # Чтобы учитывать кол-во пользователей, которые были зарегистрированы до внедрения
        # логгирования действий пользователей используется переменная start_value
        start_value = 0  # TODO: найти и вписать реальное
        counts = await self._user_action_repository.get_action_count_map_until_date(self._date)
        return start_value + counts.subscribed + counts.reactivated - counts.unsubscribed


class UserCountGraphData(object):
    """Класс, составляющий данные для графика кол-ва пользователей."""

    def __init__(self, user_action_repository: UserActionRepositoryInterface, start_value: StartValue):
        self._user_repository = user_action_repository
        self._start_value = start_value

    async def calculate(self, start_date: datetime.date, finish_date: datetime.date):
        """Расчет.

        :param start_date: datetime.date
        :param finish_date: datetime.date
        :return: dict
        """
        return_value = {}
        start_value = await self._start_value.calculate()
        actions = await self._user_repository.get_user_actions_by_date_range(start_date, finish_date)
        for date in DatesIterator(start_date, finish_date):
            return_value[date] = start_value
            # TODO: думаю можно это не группировать
            actions_grouped_by_date = [action for action in actions if action.date == date]
            self._map_to_date_users_count(date, actions_grouped_by_date, return_value)
            start_value = return_value[date]
        return return_value

    def _map_to_date_users_count(self, date, actions_grouped_by_date, return_value):
        for date_obj in actions_grouped_by_date:
            if date_obj.action in {ActionTypeEnum.SUBSCRIBED, ActionTypeEnum.REACTIVATED}:
                return_value[date] += 1
            elif date_obj.action == ActionTypeEnum.UNSUBSCRIBED:
                return_value[date] -= 1
