from asyncpg import Connection
from fastapi import APIRouter, Depends, Query, Request
from pypika import Parameter
from pypika import Query as SqlQuery
from pypika import Table
from pypika.functions import Count

from db import db_connection
from handlers.v1.schemas.ayats import AyatModel, AyatModelShort, PaginatedAyatResponse
from repositories.ayat import AyatRepository, ElementsCount
from services.ayats import NeighborsPageLinks, NextPage, PaginatedResponse, PaginatedSequence, PrevPage
from services.limit_offset_by_page_params import LimitOffsetByPageParams

router = APIRouter(prefix='/ayats')


@router.get('/', response_model=PaginatedAyatResponse)
async def get_ayats_list(
    request: Request,
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
    elements_count: ElementsCount = Depends(),
    paginated_sequence: PaginatedSequence = Depends()
) -> PaginatedAyatResponse:
    """Получить список аятов.

    :param request: Request
    :param page_num: int
    :param page_size: int
    :return: list[AyatModelShort]
    """
    ayats_table = Table('content_ayat')
    count = elements_count.update_query(
        str(SqlQuery().from_(ayats_table).select(Count('*'))),
    )
    morning_content_table = Table('content_morningcontent')
    limit, offset = LimitOffsetByPageParams(page_num, page_size).calculate()
    return await PaginatedResponse(
        count,
        (
            paginated_sequence
            .update_query(str(
                SqlQuery()
                .from_(ayats_table)
                .select(ayats_table.id, morning_content_table.day)
                .left_join(morning_content_table)
                .on(ayats_table.one_day_content_id == morning_content_table.id)
                .orderby(ayats_table.id)
                .limit(limit)
                .offset(offset)
            ))
            .update_model_to_parse(AyatModelShort)
        ),
        PaginatedAyatResponse,
        NeighborsPageLinks(
            PrevPage(page_num, request.url),
            NextPage(
                page_num,
                page_size,
                request.url,
                count,
                LimitOffsetByPageParams(page_num, page_size),
            ),
        ),
    ).get()


@router.get('/{ayat_id}/', response_model=AyatModel)
async def get_ayat_detail(
    ayat_id: int,
    ayat_repository: AyatRepository = Depends(),
) -> AyatModel:
    """Получить детальную инфу по аяту.

    :param request: Request
    :param ayat_id: int
    :return: AyatModel
    """
    return await ayat_repository.get_ayat_detail(ayat_id)
