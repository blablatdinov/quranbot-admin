from fastapi import APIRouter, Depends

from handlers.v1.schemas.auth import AuthInputData
from repositories.auth import UserRepository
from services.auth import Password, Token

router = APIRouter(prefix='/auth')


@router.post('/', status_code=201)
async def get_token(input_data: AuthInputData, user_repository: UserRepository = Depends()):
    return await Token(
        user_repository,
        input_data.username,
        Password(
            user_repository,
        ),
    ).generate(input_data.username, input_data.password)
