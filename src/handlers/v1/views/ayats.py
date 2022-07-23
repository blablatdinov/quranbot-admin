from fastapi import APIRouter, Query, Request

from handlers.v1.schemas.ayats import AyatModel, AyatModelShort, PaginatedAyatResponse
from repositories.ayat import AyatCountQuery, PaginatedSequenceQuery, ShortAyatQuery, Ayat
from services.ayats import Count, NeighborsPageLinks, NextPage, PaginatedResponse, PaginatedSequence, PrevPage
from services.limit_offset_by_page_params import LimitOffsetByPageParams

router = APIRouter(prefix='/ayats')


@router.get('/', response_model=PaginatedAyatResponse)
async def get_ayats_list(
    request: Request,
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
) -> PaginatedAyatResponse:
    """Получить список аятов.

    :param request: Request
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
        request.state.connection,
        AyatCountQuery(),
    )
    return await PaginatedResponse(
        count,
        PaginatedSequence(
            request.state.connection,
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
async def get_ayat_detail(request: Request, ayat_id: int) -> AyatModel:
    """Получить детальную инфу по аяту.

    :param ayat_id: int
    :return: AyatModel
    """
    ayat = await Ayat.from_id(request.state.connection, ayat_id)
    return ayat.to_pydantic()
