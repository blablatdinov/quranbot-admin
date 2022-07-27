import datetime
from typing import Literal

from fastapi import APIRouter, Depends, Query, Request, status
from pypika import Query as SqlQuery
from pypika import Table
from pypika.functions import Count

from handlers.v1.schemas.messages import Message, PaginatedMessagesResponse
from repositories.ayat import ElementsCount
from repositories.messages import FilteredMessageQuery, MessagesQuery, PaginatedMessagesQuery
from repositories.paginated_sequence import PaginatedSequence
from services.auth import User
from services.ayats import NeighborsPageLinks, NextPage, PaginatedResponse, PrevPage
from services.limit_offset_by_page_params import LimitOffsetByPageParams

router = APIRouter(prefix='/messages')


@router.get('/', response_model=PaginatedMessagesResponse)
async def get_messages_list(
    request: Request,
    filter_param: Literal['without_mailing', 'unknown'] = Query(default='', alias='filter'),
    page_num: int = 1,
    page_size: int = 50,
    elements_count: ElementsCount = Depends(),
    paginated_sequence: PaginatedSequence = Depends(),
    user: User = Depends(User.get_from_token),
) -> PaginatedMessagesResponse:
    """Получить сообщения.

    :param request: Request
    :param filter_param: str
    :param page_num: int
    :param page_size: int
    :param elements_count: ElementsCount
    :param paginated_sequence: PaginatedSequence
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
            PrevPage(page_num, page_size, elements_count, request.url),
            NextPage(
                page_num,
                page_size,
                request.url,
                count,
                LimitOffsetByPageParams(page_num, page_size),
            ),
        ),
    ).get()


@router.get('/{message_id}', response_model=Message)
def get_message(message_id: int) -> Message:
    """Получить сообщения.

    :param message_id: int
    :return: PaginatedResponse
    """
    return Message(
        id=message_id,
        message_source='from 23343',
        sending_date=datetime.datetime(1000, 1, 1),
        message_id=1,
        text='Hello...',
    )


@router.delete('/{message_id}/delete-from-chat', status_code=status.HTTP_204_NO_CONTENT)
def delete_message_from_telegram(message_id: int):
    """Получить сообщения.

    :param message_id: int
    :return: None
    """
    return  # noqa: WPS324
