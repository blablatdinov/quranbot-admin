"""Обработчики HTTP запросов для работы с файлами.

Functions:
    get_files
"""
from fastapi import APIRouter, Depends, Query, Request
from pypika import Query as SqlQuery
from pypika.functions import Count

from handlers.v1.schemas.files import FileModel, OrderingParams, PaginatedFileResponse
from repositories.file import FilePaginatedQuery, OrderedFileQuery
from repositories.paginated_sequence import ElementsCount, PaginatedSequence
from services.limit_offset_by_page_params import LimitOffsetByPageParams
from services.paginating import NeighborsPageLinks, NextPage, PaginatedResponse, PrevPage, UrlWithoutQueryParams

router = APIRouter(prefix='/files')


@router.get('/')
async def get_files(
    request: Request,
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
    elements_count: ElementsCount = Depends(),
    order_param: OrderingParams = Query('id', alias='ordering'),
    paginated_sequence: PaginatedSequence = Depends(),
):
    """Получить список файлов с пагинацией.

    :param request: Request
    :param page_num: int
    :param page_size: int
    :param elements_count: ElementsCount
    :param order_param: OrderingParams
    :param paginated_sequence: PaginatedSequence
    :return: PaginatedResponse
    """
    count = elements_count.update_query(
        str(SqlQuery().from_('content_file').select(Count('*'))),
    )
    return await PaginatedResponse(
        count,
        (
            paginated_sequence
            .update_query(
                OrderedFileQuery(
                    FilePaginatedQuery(
                        LimitOffsetByPageParams(page_num, page_size),
                    ),
                    order_param,
                ),
            )
            .update_model_to_parse(FileModel)
        ),
        PaginatedFileResponse,
        NeighborsPageLinks(
            PrevPage(
                page_num,
                page_size,
                count,
                UrlWithoutQueryParams(request),
            ),
            NextPage(
                page_num,
                page_size,
                UrlWithoutQueryParams(request),
                count,
                LimitOffsetByPageParams(page_num, page_size),
            ),
        ),
    ).get()
