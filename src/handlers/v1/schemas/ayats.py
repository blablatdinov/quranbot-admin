"""Схемы для аятов.

Classes:
    FileModel
    AyatModel
    AyatModelShort
    PaginatedAyatResponse
"""
from typing import Optional

from pydantic import BaseModel


class FileModel(BaseModel):
    """Модель файла."""

    id: int
    link: str
    telegram_file_id: str
    name: Optional[str]


class AyatModel(BaseModel):
    """Модель аята."""

    id: int
    additional_content: str
    content: str  # noqa: WPS110
    arab_text: str
    trans: str
    sura_num: int
    ayat_num: str
    html: str
    audio_file: FileModel
    mailing_day: int


class AyatModelShort(BaseModel):
    """Урезанная модель аята."""

    id: int
    content: str  # noqa: WPS110
    arab_text: str
    trans: str
    sura_num: int
    ayat_num: str
    audio_file_link: str


class PaginatedAyatResponse(BaseModel):
    """Модель ответа списка аятов с пагинацией."""

    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[AyatModelShort]  # noqa: WPS110 api schema field name
