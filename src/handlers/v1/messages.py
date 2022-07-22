from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter(prefix='/messages')


class Message(BaseModel):
    """Модель сообщения."""

    id: int


class PaginatedResponse(BaseModel):
    """Модель ответа сообщений с пагинацией."""

    count: int
    next: str
    prev: str
    results: list[Message]  # noqa: WPS110


@router.get('/', response_model=PaginatedResponse)
def get_messages_list(request: Request, page: int = 1) -> PaginatedResponse:
    """Получить сообщения.

    :param request: Request
    :param page: int
    :return: PaginatedResponse
    """
    return PaginatedResponse(
        count=2,
        next='{0}?page={1}'.format(request.url.path, page + 1),
        prev='{0}?page={1}'.format(request.url.path, page - 1),
        results=[Message(id=1), Message(id=2)],
    )
