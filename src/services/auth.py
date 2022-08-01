import datetime

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import pbkdf2_sha256
from pydantic import ValidationError

from exceptions import UserNotFoundError, IncorrectCredentialsError
from handlers.v1.schemas.auth import TokenResponse
from repositories.auth import UserRepository, UserRepositoryInterface, UserSchema
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/')


class PasswordInterface(object):
    """Интерфейс пароля."""

    async def check(self, username, password):
        """Проверить пароль.

        :param username: str
        :param password: str
        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError


class Password(PasswordInterface):
    """Класс, представляющий пароль."""

    _user_repository: UserRepositoryInterface
    _raw_password: str

    def __init__(self, user_repository: UserRepository = Depends()):
        self._user_repository = user_repository

    async def check(self, username, password) -> bool:
        """Проверка пароля.

        :param username: str
        :param password: str
        :return: bool
        """
        try:
            user = await self._user_repository.get_by_username(username)
        except UserNotFoundError as error:
            raise IncorrectCredentialsError from error
        splitted_password_data = user.password.split('$')
        password_hash_id_storage = splitted_password_data[-1][:-1].replace('+', '.')
        input_password_hash = pbkdf2_sha256.hash(
            password, rounds=int(splitted_password_data[1]), salt=splitted_password_data[2].encode('utf8'),
        ).split('$')[-1]
        return input_password_hash == password_hash_id_storage


class AuthService(object):
    """Сервис авторизации."""

    _user_repository: UserRepositoryInterface

    def __init__(self, user_repository: UserRepositoryInterface, username: str, password: Password):
        self._user_repository = user_repository
        self._username = username
        self._password = password

    async def generate(self, username: str, raw_password: str):
        """Сгенерировать JWT токен.

        :param username: str
        :param raw_password: str
        :return: TokenResponse
        :raises HTTPException: if password incorrect
        """
        password_valid = await self._password.check(username, raw_password)
        if not password_valid:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'incorrect credentials')
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
    """Токен."""

    _token: str

    def __init__(self, token: str):
        self._token = token

    def verify_token(self) -> UserSchema:
        """Проверить токен.

        :return: UserSchema
        :raises exception: if credentials invalid
        """
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
        except JWTError as error:
            raise exception from error

        user_data = payload.get('user')

        try:
            user = UserSchema.parse_obj(user_data)
        except ValidationError as validation_error:
            raise exception from validation_error

        return user


class User(object):
    """Пользователь."""

    @classmethod
    def get_from_token(cls, token: str = Depends(oauth2_scheme)):
        """Получить пользователя по токену.

        :param token: str
        :return: Token
        """
        return Token(token).verify_token()
