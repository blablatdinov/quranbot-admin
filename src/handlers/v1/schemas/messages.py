import datetime
from typing import Optional

from pydantic.main import BaseModel


class Message(BaseModel):
    """Модель сообщения."""

    id: int
    message_source: str
    sending_date: datetime.datetime
    message_id: int
    text: str


class PaginatedMessagesResponse(BaseModel):
    """Модель ответа сообщений с пагинацией."""

    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[Message]  # noqa: WPS110
