from typing import Optional

from asyncpg import Connection
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, parse_obj_as

from db import db_connection
from services.ayats import ShortAyatQuery, AyatCountQuery, PaginatedSequenceQuery, Count, PaginatedSequence, \
    PaginatedResponse, PaginatedAyatResponse, AyatModelShort

router = APIRouter(prefix='/ayats')


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


@router.get('/', response_model=PaginatedAyatResponse)
async def get_ayats_list(
    request: Request,
    db_connenction: Connection = Depends(db_connection),
    page_num: int = 1,
    page_size: int = 50,
) -> PaginatedAyatResponse:
    """Получить список аятов.

    :return: list[AyatModelShort]
    """
    return await PaginatedResponse(
        page_num,
        page_size,
        Count(
            db_connenction,
            AyatCountQuery(),
        ),
        PaginatedSequence(
            db_connenction,
            PaginatedSequenceQuery(
                ShortAyatQuery(),
                page_num,
                page_size,
            ),
            AyatModelShort,
        ),
        '{0}://{1}:{2}{3}'.format(request.url.scheme, request.url.hostname, request.url.port, request.url.path)
    ).get()


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
