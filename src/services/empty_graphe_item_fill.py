import datetime

from repositories.messages import MessageRepositoryInterface
from handlers.v1.schemas.messages import MessageGraphDataItem


class GraphZeroValueItemSave(object):

    def __init__(self, message_repository: MessageRepositoryInterface):
        self._message_repository = message_repository

    async def get_messages_for_graph(
        self,
        start_date: datetime.date,
        finish_date: datetime.date,
    ) -> list[MessageGraphDataItem]:
        db_query_result = await self._message_repository.get_messages_for_graph(start_date, finish_date)
        while start_date < finish_date:
            if start_date not in db_query_result:
                db_query_result[start_date] = 0
            start_date += datetime.timedelta(days=1)
        return sorted(
            [
                MessageGraphDataItem(date=date, messages_count=messages_count)
                for date, messages_count in db_query_result.items()
            ],
            key=lambda x: x.date
        )
