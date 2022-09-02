"""Модуль, содержащий обработчик события из очереди сообщений.

Classes:
    UserSubscribedEvent
"""
import uuid

from repositories.auth import UserInsertSchema, UserRepositoryInterface
from repositories.user_action import UserActionEnum, UserActionRepositoryInterface, UserActionSchema


class UserSubscribedEvent(object):
    """Событие подписки нового пользователя."""

    event_name = 'User.Subscribed'

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
        await self._user_repository.create(UserInsertSchema(
            chat_id=event_data['user_id'],
            day=2,
        ))
        await self._user_action_repository.save(UserActionSchema(
            user_action_id=uuid.uuid4(),
            date_time=event_data['date_time'],
            action=UserActionEnum.subscribed,
            user_id=event_data['user_id'],
        ))
