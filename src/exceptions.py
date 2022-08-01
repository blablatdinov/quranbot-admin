from http.client import HTTPException


class UserNotFoundError(Exception):
    pass


class IncorrectCredentialsError(HTTPException):

    status_code = 400
