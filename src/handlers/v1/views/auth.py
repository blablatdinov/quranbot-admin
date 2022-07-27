from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from repositories.auth import UserRepository
from services.auth import Password, AuthService

router = APIRouter(prefix='/auth')


@router.post('/', status_code=201)
async def get_token(auth_data: OAuth2PasswordRequestForm = Depends(), user_repository: UserRepository = Depends()):
    return await AuthService(
        user_repository,
        auth_data.username,
        Password(
            user_repository,
        ),
    ).generate(auth_data.username, auth_data.password)
