from fastapi import APIRouter

from handlers.v1.schemas.auth import AuthInputData

router = APIRouter(prefix='/auth')


@router.post('/', status_code=201)
async def get_token(input_data: AuthInputData):
    pass
