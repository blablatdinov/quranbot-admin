"""Модуль схем для работы с файлами.

Classes:
    OrderingParams
    FileModel
    PaginatedFileResponse
"""
import enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class OrderingParams(str, enum.Enum):  # noqa: WPS600
    """Параметры для сортировки."""

    id_asc = 'id'
    id_desc = '-id'
    link_asc = 'link_to_file'
    link_desc = '-link_to_file'


class FileModel(BaseModel):
    """Модель файла."""

    id: UUID
    link: Optional[str]  # TODO: must replace to Optional[pydantic.AnyUrl]
    telegram_file_id: Optional[str]
    name: Optional[str]


class PaginatedFileResponse(BaseModel):
    """Модель ответа списка файлов с пагинацией."""

    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[FileModel]  # noqa: WPS110 api schema field name
