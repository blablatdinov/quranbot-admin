"""Обработчики HTTP запросов для аутентификации.

Functions:
    get_token
    get_users_count
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from handlers.v1.schemas.auth import TokenResponse
from repositories.auth import UserRepository
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
