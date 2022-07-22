from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix='/ayats')


class AyatModelShort(BaseModel):
    """Урезанная модель аята."""

    id: int
    mailing_day: int


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


@router.get('/', response_model=list[AyatModelShort])
def get_ayats_list() -> list[AyatModelShort]:
    """Получить список аятов.

    :return: list[AyatModelShort]
    """
    return [AyatModelShort(id=1, mailing_day=1)]


@router.get('/{ayat_id}', response_model=AyatModel)
def get_ayat_detail(ayat_id: int) -> AyatModel:
    """Получить детальную инфу по аяту.

    :param ayat_id: int
    :return: AyatModel
    """
    return AyatModel(
        id=1,
        additional_content='additional content content',
        content='ayat content',
        arab_text='arab text',
        trans='transliteration',
        sura_num=10,
        ayat_num='1,2',
        html='<html></html>',
        audio_file='link',
        mailing_day=5,
    )
