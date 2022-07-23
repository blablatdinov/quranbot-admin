import datetime
from typing import Literal

from fastapi import APIRouter, Query, Request, status

from handlers.v1.schemas.messages import PaginatedMessagesResponse, Message
from repositories.ayat import Count, PaginatedSequenceQuery
from repositories.messages import MessagesCountQuery, ShortMessageQuery
from repositories.paginated_sequence import PaginatedSequence
from services.ayats import NeighborsPageLinks, PrevPage, NextPage, PaginatedResponse
from services.limit_offset_by_page_params import LimitOffsetByPageParams

router = APIRouter(prefix='/messages')


@router.get('/', response_model=PaginatedMessagesResponse)
async def get_messages_list(
    request: Request,
    filter_param: Literal['without_mailing', 'unknown'] = Query(default='', alias='filter'),
    page_num: int = 1,
    page_size: int = 50,
) -> PaginatedMessagesResponse:
    """Получить сообщения.

    :param request: Request
    :param filter_param: str
    :param page: int
    :return: PaginatedResponse
    """
    url = '{0}://{1}:{2}{3}'.format(
        request.url.scheme,
        request.url.hostname,
        request.url.port,
        request.url.path,
    )
    count = Count(
        request.state.connection,
        MessagesCountQuery(),
    )
    return await PaginatedResponse(
        count,
        PaginatedSequence(
            request.state.connection,
            PaginatedSequenceQuery(
                ShortMessageQuery(),
                LimitOffsetByPageParams(page_num, page_size),
            ),
            Message,
        ),
        PaginatedMessagesResponse,
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
