import datetime

from services.empty_graphe_item_fill import GraphZeroValueItemSave
from handlers.v1.schemas.messages import MessageGraphDataItem
from repositories.messages import MessageRepositoryInterface


class MessageRepositoryMock(MessageRepositoryInterface):

    async def get_messages_for_graph(self, start_date, finish_date):
        return [MessageGraphDataItem(date=datetime.date(2022, 8, 6), messages_count=1)]


async def test():
    got = await GraphZeroValueItemSave(MessageRepositoryMock()).get_messages_for_graph(
        datetime.date(2022, 7, 6),
        datetime.date(2022, 8, 6),
    )
