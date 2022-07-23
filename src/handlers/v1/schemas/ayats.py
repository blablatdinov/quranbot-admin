from typing import Optional

from pydantic.main import BaseModel


class File(BaseModel):
    id: int
    link: str
    file_id: str
    name: str


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
    audio_file: File
    mailing_day: int


class AyatModelShort(BaseModel):
    """Урезанная модель аята."""

    id: int
    mailing_day: Optional[int]


class PaginatedAyatResponse(BaseModel):
    """Модель ответа списка аятов с пагинацией."""

    count: int
    next: Optional[str]
    prev: Optional[str]
    results: list[AyatModelShort]  # noqa: WPS110 api schema field name
