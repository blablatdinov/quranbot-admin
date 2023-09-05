"""Обработчики HTTP запросов для работы с файлами.

Functions:
    get_files
    post_file
"""
from databases import Database
from fastapi import APIRouter, Depends, Query, UploadFile, status

from db.connection import db_connection
from integrations.queue_integration import NatsIntegration
from services.file import DiskFile, FileTriggeredToDownload
from services.files_paginated_response import FilesCount, FilesPaginatedResponse
from services.limit_offset_by_page_params import LimitOffset
from services.pg_files_list import PgFilesList

router = APIRouter(prefix='/files')


@router.get('/')
async def get_files(
    page_num: int = Query(default=1, ge=1),
    page_size: int = 50,
    pgsql: Database = Depends(db_connection),
):
    """Получить список файлов с пагинацией.

    :param page_num: int
    :param page_size: int
    :param pgsql: Database
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
