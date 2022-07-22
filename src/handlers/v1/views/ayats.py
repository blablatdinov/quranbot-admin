from asyncpg import Connection
from fastapi import APIRouter, Depends, Request

from db import db_connection
from handlers.v1.schemas.ayats import AyatModel, AyatModelShort
from repositories.ayat import AyatCountQuery, ShortAyatQuery, PaginatedSequenceQuery
from services.ayats import Count, PaginatedAyatResponse, PaginatedResponse, PaginatedSequence, PrevPage, NextPage
from services.limit_offset_by_page_params import LimitOffsetByPageParams

router = APIRouter(prefix='/ayats')


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
    url = '{0}://{1}:{2}{3}'.format(request.url.scheme, request.url.hostname, request.url.port, request.url.path)
    count = Count(
        db_connenction,
        AyatCountQuery(),
    )
    return await PaginatedResponse(
        count,
        PaginatedSequence(
            db_connenction,
            PaginatedSequenceQuery(
                ShortAyatQuery(),
                LimitOffsetByPageParams(page_num, page_size),
            ),
            AyatModelShort,
        ),
        PaginatedAyatResponse,
        PrevPage(page_num, url),
        NextPage(
            page_num,
            page_size,
            url,
            count,
            LimitOffsetByPageParams(page_num, page_size)
        ),
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
