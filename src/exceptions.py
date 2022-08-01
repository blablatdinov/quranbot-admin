from http.client import HTTPException


class UserNotFoundError(Exception):
    """Исключение, вызываемое если пользователь не найден."""

    def __str__(self):
        """Строковое представление.

        :return: str
        """
        return 'User not found'


class IncorrectCredentialsError(HTTPException):
    """Исключение, вызываемое при невалидных данных для доступа."""

    status_code = 400
