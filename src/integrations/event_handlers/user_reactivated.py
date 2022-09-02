"""Модуль, содержащий обработчик события из очереди сообщений.

Classes:
    UserReactivatedEvent
"""
import uuid

from repositories.auth import UserRepositoryInterface
from repositories.user_action import UserActionEnum, UserActionRepositoryInterface, UserActionSchema


class UserReactivatedEvent(object):
    """Событие создания действия пользователя."""

    event_name = 'User.Reactivated'

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        user_action_repository: UserActionRepositoryInterface,
    ):
        """Конструктор класса.

        :param user_repository: UserRepositoryInterface
        :param user_action_repository: UserActionRepositoryInterface
        """
        self._user_action_repository = user_action_repository
        self._user_repository = user_repository

    async def handle_event(self, event_data):
        """Обработка события.

        :param event_data: dict
        """
        await self._user_repository.update_status(event_data['user_id'], to=True)
        await self._user_action_repository.save(UserActionSchema(
            user_action_id=uuid.uuid4(),
            date_time=event_data['date_time'],
            action=UserActionEnum.unsubscribed,
            user_id=event_data['user_id'],
        ))
