"""Обработчики HTTP запросов для работы с сообщенияеми.

Functions:
    get_messages_list
    get_message
    delete_message_from_telegram
    get_count_graph
"""
import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query, Request, status
from pypika import Query as SqlQuery
from pypika import Table
from pypika.functions import Count

from handlers.v1.schemas.messages import (
    DeleteMessagesRequest,
    Message,
    MessageGraphDataItem,
    PaginatedMessagesResponse,
)
from repositories.auth import UserSchema
from repositories.messages import FilteredMessageQuery, MessageRepository, MessagesQuery, PaginatedMessagesQuery
from repositories.paginated_sequence import ElementsCount, PaginatedSequence
from services.auth import User
from services.date_range import DateRange
from services.limit_offset_by_page_params import LimitOffsetByPageParams
from services.messages import Messages
from services.paginating import NeighborsPageLinks, NextPage, PaginatedResponse, PrevPage, UrlWithoutQueryParams
from services.start_date_dependency import start_date_dependency

router = APIRouter(prefix='/messages')


@router.get('/', response_model=PaginatedMessagesResponse)
async def get_messages_list(
    request: Request,
    filter_param: Literal['without_mailing', 'unknown'] = Query(default='', alias='filter'),
    page_num: int = 1,
    page_size: int = 50,
    elements_count: ElementsCount = Depends(),
    paginated_sequence: PaginatedSequence = Depends(),
    user: UserSchema = Depends(User.get_from_token),
) -> PaginatedMessagesResponse:
    """Получить сообщения.

    :param request: Request
    :param filter_param: str
    :param page_num: int
    :param page_size: int
    :param elements_count: ElementsCount
    :param paginated_sequence: PaginatedSequence
    :param user: UserSchema
    :return: PaginatedResponse
    """
    messages_table = Table('bot_init_message')
    count = elements_count.update_query(
        str(
            SqlQuery()
            .from_(messages_table)
            .select(Count('*')),
        ),
    )
    return await PaginatedResponse(
        count,
        (
            paginated_sequence
            .update_query(
                PaginatedMessagesQuery(
                    FilteredMessageQuery(
                        MessagesQuery(),
                        filter_param,
                    ),
                    LimitOffsetByPageParams(page_num, page_size),
                ),
            )
            .update_model_to_parse(Message)
        ),
        PaginatedMessagesResponse,
        NeighborsPageLinks(
            PrevPage(page_num, page_size, count, UrlWithoutQueryParams(request)),
            NextPage(
                page_num,
                page_size,
                UrlWithoutQueryParams(request),
                count,
                LimitOffsetByPageParams(page_num, page_size),
            ),
        ),
    ).get()


@router.get('/{message_id}', response_model=Message)
def get_message(message_id: int, user: UserSchema = Depends(User.get_from_token)) -> Message:
    """Получить сообщения.

    :param message_id: int
    :param user: UserSchema
    :return: PaginatedResponse
    """
    return Message(
        id=message_id,
        message_source='from 23343',
        sending_date=datetime.datetime(1000, 1, 1),
        message_id=1,
        text='Hello...',
    )


@router.delete('/', status_code=status.HTTP_201_CREATED)
async def delete_message_from_telegram(
    input_data: DeleteMessagesRequest,
    messages_service: Messages = Depends(),
    user: UserSchema = Depends(User.get_from_token),
):
    """Удалить сообщения.

    Используется статус 201, т. к. с 204 проблемы (см. https://github.com/tiangolo/fastapi/issues/717)

    :param input_data: DeleteMessagesRequest
    :param messages_service: Messages
    :param user: UserSchema
    """
    await messages_service.delete(input_data.message_ids)


@router.get('/count-graph/')
async def get_count_graph(
    finish_date: datetime.date = None,
    start_date: datetime.date = Depends(start_date_dependency),
    messages_repository: MessageRepository = Depends(),
) -> list[MessageGraphDataItem]:
    """Получить данные для графика кол-ва сообщений.

    :param finish_date: datetime.date
    :param start_date: datetime.date
    :param messages_repository: MessageRepository
    :return: list[MessageGraphDataItem]
    """
    date_range = DateRange(start_date, finish_date)
    return await messages_repository.get_messages_for_graph(date_range.start_date, date_range.finish_date)
