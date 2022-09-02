import datetime

from integrations.queue_integration import UserUnsubscribedEvent
from repositories.auth import UserRepositoryInterface
from repositories.user_action import UserActionRepositoryInterface, UserActionSchema, UserActionEnum


class UserRepositoryMock(UserRepositoryInterface):

    is_active = True

    async def update_status(self, chat_id: int, to: bool):
        self.is_active = to


class UserActionRepositoryMock(UserActionRepositoryInterface):

    storage = []

    async def save(self, user_action: UserActionSchema):
        self.storage.append(user_action)


async def test():
    user_repo = UserRepositoryMock()
    user_action_repo = UserActionRepositoryMock()
    await UserUnsubscribedEvent(user_repo, user_action_repo).handle_event({
        'user_id': 3324,
        'date_time': datetime.datetime(2050, 6, 7),
    })

    assert user_repo.is_active is False
    assert user_action_repo.storage[0].date_time == datetime.datetime(2050, 6, 7)
    assert user_action_repo.storage[0].action == UserActionEnum.unsubscribed
    assert user_action_repo.storage[0].user_id == 3324
