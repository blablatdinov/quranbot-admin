import datetime
from typing import Literal

from fastapi import APIRouter, Query, Request, status
from pydantic import BaseModel

router = APIRouter(prefix='/messages')


class Message(BaseModel):
    """Модель сообщения."""

    id: int
    message_source: str
    sending_date: datetime.datetime
    message_id: int
    text: str


class PaginatedResponse(BaseModel):
    """Модель ответа сообщений с пагинацией."""

    count: int
    next: str
    prev: str
    results: list[Message]  # noqa: WPS110


@router.get('/', response_model=PaginatedResponse)
def get_messages_list(
    request: Request,
    filter_param: Literal['without_mailing', 'unknown'] = Query(default='', alias='filter'),
    page: int = 1,
) -> PaginatedResponse:
    """Получить сообщения.

    :param request: Request
    :param filter_param: str
    :param page: int
    :return: PaginatedResponse
    """
    return PaginatedResponse(
        count=2,
        next='{0}?page={1}'.format(request.url.path, page + 1),
        prev='{0}?page={1}'.format(request.url.path, page - 1),
        results=[
            Message(
                id=1,
                message_source='from 23343',
                sending_date=datetime.datetime(1000, 1, 1),
                message_id=1,
                text='Hello...',
            ),
            Message(
                id=2,
                message_source='Mailing (45)',
                sending_date=datetime.datetime(1000, 1, 1),
                message_id=10,
                text='Bye...',
            ),
        ],
    )


@router.get('/{message_id}', response_model=Message)
def get_message(message_id: int) -> Message:
    """Получить сообщения.

    :param message_id: int
    :return: PaginatedResponse
    """
    return Message(
        id=message_id,
        message_source='from 23343',
        sending_date=datetime.datetime(1000, 1, 1),
        message_id=1,
        text='Hello...',
    )


@router.delete('/{message_id}/delete-from-chat', status_code=status.HTTP_204_NO_CONTENT)
def delete_message_from_telegram(message_id: int):
    """Получить сообщения.

    :param message_id: int
    :return: None
    """
    return  # noqa: WPS324
