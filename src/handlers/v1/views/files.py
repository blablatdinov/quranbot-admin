"""Обработчики HTTP запросов для работы с файлами.

Functions:
    get_files
    post_file
"""
from databases import Database
from fastapi import APIRouter, Depends, Query, Request, UploadFile, status
from pypika import Query as SqlQuery
from pypika.functions import Count

from db.connection import db_connection
from handlers.v1.schemas.files import FileModel, OrderingParams, PaginatedFileResponse
from integrations.queue_integration import NatsIntegration
from repositories.file import FilePaginatedQuery, OrderedFileQuery
from repositories.paginated_sequence import ElementsCount, PaginatedSequence
from services.file import DiskFile, FileTriggeredToDownload
from services.files_paginated_response import FilesPaginatedResponse, FilesCount
from services.limit_offset_by_page_params import LimitOffset
from services.paginating import NeighborsPageLinks, NextPage, PaginatedResponse, PrevPage, UrlWithoutQueryParams
from services.pg_files_list import PgFilesList

router = APIRouter(prefix='/files')


@router.get('/')
async def get_files(
    request: Request,
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
    elements_count: ElementsCount = Depends(),
    order_param: OrderingParams = Query('id', alias='ordering'),
    paginated_sequence: PaginatedSequence = Depends(),
    pgsql: Database = Depends(db_connection),
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
    return await FilesPaginatedResponse(
        FilesCount(pgsql),
        PgFilesList(
            pgsql,
            LimitOffset.int_ctor(page_num, page_size),
        ),
    ).build()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def post_file(
    file: UploadFile,  # noqa: WPS110 name used in api schema
    disk_file: DiskFile = Depends(),
    nats_integration: NatsIntegration = Depends(),
):
    """Метод для создания файла.

    :param file: UploadFile
    :param disk_file: DiskFile
    :param nats_integration: NatsIntegration
    """
    await FileTriggeredToDownload(disk_file, nats_integration).save(file.filename, await file.read())
