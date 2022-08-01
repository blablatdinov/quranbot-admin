"""Обработчики HTTP запросов для аутентификации.

Functions:
    get_token
    get_users_count
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pypika import Query as SqlQuery
from pypika.functions import Count

from handlers.v1.schemas.auth import TokenResponse, UsersCountGithubBadge
from repositories.auth import UserRepository
from repositories.paginated_sequence import ElementsCount
from services.auth import AuthService, Password

router = APIRouter(prefix='/auth')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def get_token(
    auth_data: OAuth2PasswordRequestForm = Depends(),
    user_repository: UserRepository = Depends(),
    password_instance: Password = Depends(),
) -> TokenResponse:
    """Получить JWT токен.

    :param auth_data: OAuth2PasswordRequestForm
    :param user_repository: UserRepository
    :param password_instance: Password
    :return: TokenResponse
    """
    return await AuthService(
        user_repository,
        auth_data.username,
        password_instance,
    ).generate(auth_data.username, auth_data.password)


@router.get('/users-count-github-badge/')
async def get_users_count(elements_count: ElementsCount = Depends()) -> UsersCountGithubBadge:
    """Получить кол-во пользователей.

    :param elements_count: ElementsCount
    :return: UsersCountGithubBadge
    """
    count = elements_count.update_query(
        str(SqlQuery().from_('bot_init_subscriber').select(Count('*'))),
    )
    return UsersCountGithubBadge(
        label='users count',
        message=await count.get(),
    )
