"""Обработчики HTTP запросов для просмотра аятов.

Functions:
    get_ayats_list
    get_ayat_detail
"""
from databases import Database
from fastapi import APIRouter, Depends, Query

from db.connection import db_connection
from handlers.v1.schemas.ayats import AyatModel, PaginatedAyatResponse
from services.ayat_detail_response import AyatDetailResponse
from services.ayats_count import AyatsCount
from services.ayats_paginated_response import AyatsPaginatedResponse
from services.limit_offset_by_page_params import LimitOffset
from services.pg_ayats_list import PgAyatsList

router = APIRouter(prefix='/ayats')


@router.get('/', response_model=PaginatedAyatResponse)
async def get_ayats_list(
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
    pgsql: Database = Depends(db_connection),
) -> PaginatedAyatResponse:
    """Получить список аятов.

    :param page_num: int
    :param page_size: int
    :param pgsql: Database
    :return: PaginatedAyatResponse
    """
    return await AyatsPaginatedResponse(
        AyatsCount(pgsql),
        PgAyatsList(pgsql, LimitOffset(page_num, page_size)),
    ).build()


@router.get('/{ayat_id}/', response_model=AyatModel)
async def get_ayat_detail(
    ayat_id: int,
    pgsql: Database = Depends(db_connection),
) -> AyatModel:
    """Получить детальную инфу по аяту.

    :param ayat_id: int
    :param pgsql: Database
    :return: AyatModel
    """
    return await AyatDetailResponse(pgsql, ayat_id).build()
