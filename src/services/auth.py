import datetime

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError
from pydantic import ValidationError

from handlers.v1.schemas.auth import TokenResponse
from repositories.auth import UserRepositoryInterface, UserRepository, UserSchema
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/')


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


class AuthService(object):

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
        return TokenResponse(access_token=token)


class Token(object):

    _token: str

    def __init__(self, token: str):
        self._token = token

    def verify_token(self) -> UserSchema:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                self._token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = UserSchema.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user


class User(object):

    @classmethod
    def get_from_token(cls, token: str = Depends(oauth2_scheme)):
        return Token(token).verify_token()
