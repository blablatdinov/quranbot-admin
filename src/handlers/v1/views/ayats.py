from asyncpg import Connection
from fastapi import APIRouter, Depends, Query, Request

from db import db_connection
from handlers.v1.schemas.ayats import AyatModel, AyatModelShort, PaginatedAyatResponse
from repositories.ayat import AyatCountQuery, PaginatedSequenceQuery, ShortAyatQuery
from services.ayats import Count, NeighborsPageLinks, NextPage, PaginatedResponse, PaginatedSequence, PrevPage
from services.limit_offset_by_page_params import LimitOffsetByPageParams

router = APIRouter(prefix='/ayats')


@router.get('/', response_model=PaginatedAyatResponse)
async def get_ayats_list(
    request: Request,
    connection: Connection = Depends(db_connection),
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
) -> PaginatedAyatResponse:
    """Получить список аятов.

    :param request: Request
    :param connection: Connection
    :param page_num: int
    :param page_size: int
    :return: list[AyatModelShort]
    """
    url = '{0}://{1}:{2}{3}'.format(
        request.url.scheme,
        request.url.hostname,
        request.url.port,
        request.url.path,
    )
    count = Count(
        connection,
        AyatCountQuery(),
    )
    return await PaginatedResponse(
        count,
        PaginatedSequence(
            connection,
            PaginatedSequenceQuery(
                ShortAyatQuery(),
                LimitOffsetByPageParams(page_num, page_size),
            ),
            AyatModelShort,
        ),
        PaginatedAyatResponse,
        NeighborsPageLinks(
            PrevPage(page_num, url),
            NextPage(
                page_num,
                page_size,
                url,
                count,
                LimitOffsetByPageParams(page_num, page_size),
            ),
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
