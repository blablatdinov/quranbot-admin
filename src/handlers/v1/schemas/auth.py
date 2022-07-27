from pydantic import BaseModel


class AuthInputData(BaseModel):
    """Схема данных для авторизации."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Схема ответа с токеном."""

    access_token: str
    token_type: str = 'bearer'
