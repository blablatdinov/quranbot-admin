from fastapi import APIRouter, Depends, Query, Request
from pypika import Query as SqlQuery
from pypika.functions import Count

from handlers.v1.schemas.ayats import AyatModel, AyatModelShort, PaginatedAyatResponse
from repositories.ayat import AyatPaginatedQuery, AyatRepository, ElementsCount
from repositories.paginated_sequence import PaginatedSequence
from services.ayats import NeighborsPageLinks, NextPage, PaginatedResponse, PrevPage
from services.limit_offset_by_page_params import LimitOffsetByPageParams

router = APIRouter(prefix='/ayats')


@router.get('/', response_model=PaginatedAyatResponse)
async def get_ayats_list(
    request: Request,
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
    elements_count: ElementsCount = Depends(),
    paginated_sequence: PaginatedSequence = Depends(),
) -> PaginatedAyatResponse:
    """Получить список аятов.

    :param request: Request
    :param page_num: int
    :param page_size: int
    :param elements_count: ElementsCount
    :param paginated_sequence: PaginatedSequence
    :return: list[AyatModelShort]
    """
    count = elements_count.update_query(
        str(SqlQuery().from_('content_ayat').select(Count('*'))),
    )
    LimitOffsetByPageParams(page_num, page_size)
    return await PaginatedResponse(
        count,
        (
            paginated_sequence
            .update_query(
                AyatPaginatedQuery(
                    LimitOffsetByPageParams(page_num, page_size),
                ),
            )
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

    :param ayat_id: int
    :param ayat_repository: AyatRepository
    :return: AyatModel
    """
    return await ayat_repository.get_ayat_detail(ayat_id)
