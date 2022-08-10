from typing import Optional

from pydantic import BaseModel, AnyUrl


class FileModel(BaseModel):
    """Модель файла."""

    id: int
    link: AnyUrl
    telegram_file_id: str
    name: Optional[str]


class PaginatedFileResponse(BaseModel):
    """Модель ответа списка файлов с пагинацией."""

    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[FileModel]  # noqa: WPS110 api schema field name
