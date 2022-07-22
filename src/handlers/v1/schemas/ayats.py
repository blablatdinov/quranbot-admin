from typing import Optional

from pydantic.main import BaseModel


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
    audio_file: str  # TODO: AudioFileModel
    mailing_day: int


class AyatModelShort(BaseModel):
    """Урезанная модель аята."""

    id: int
    mailing_day: Optional[int]
