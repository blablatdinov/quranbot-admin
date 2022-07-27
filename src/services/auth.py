import datetime

from fastapi import Depends
from fastapi.exceptions import HTTPException
from passlib.hash import pbkdf2_sha256
from jose import jwt

from handlers.v1.schemas.auth import TokenResponse
from repositories.auth import UserRepositoryInterface, UserRepository
from settings import settings


class Password(object):

    _user_repository: UserRepositoryInterface
    _raw_password: str

    def __init__(self, user_repository: UserRepository = Depends()):
        self._user_repository = user_repository

    async def check(self, username, password):
        user = await self._user_repository.get_by_username(username)
        splitted_password_data = user.password.split('$')
        password_hash_id_storage = splitted_password_data[-1][:-1].replace('+', '.')
        input_password_hash = pbkdf2_sha256.hash(
            password, rounds=int(splitted_password_data[1]), salt=splitted_password_data[2].encode('utf8')
        ).split('$')[-1]
        return input_password_hash == password_hash_id_storage


class Token(object):

    _user_repository: UserRepositoryInterface

    def __init__(self, user_repository: UserRepositoryInterface, username: str, password: Password):
        self._user_repository = user_repository
        self._username = username
        self._password = password

    async def generate(self, username: str, raw_password: str):
        password_valid = await self._password.check(username, raw_password)
        if not password_valid:
            raise HTTPException(401, 'incorrect credentials')
        user_data = await self._user_repository.get_by_username(username)
        now = datetime.datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + datetime.timedelta(seconds=settings.JWT_EXPIRES_S),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        return TokenResponse(token=token)
