from pydantic import BaseModel


class AuthInputData(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    type: str = 'access'
    token: str
