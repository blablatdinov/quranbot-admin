"""Схемы для аутентификации.

Classes:
    AuthInputData
    TokenResponse
    UsersCountGithubBadge
"""
from pydantic import BaseModel
from pydantic.fields import Field


class AuthInputData(BaseModel):
    """Схема данных для авторизации."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Схема ответа с токеном."""

    access_token: str
    token_type: str = 'bearer'


class UsersCountGithubBadge(BaseModel):
    """Схема бейджика для README.md .

    https://shields.io/endpoint
    """

    schema_version: int = Field(1, alias='schemaVersion')
    label: str
    message: str
    color: str = 'informational'
