import datetime

from repositories.messages import MessageRepositoryInterface


class GraphZeroValueItemSave(object):

    def __init__(self, message_repository: MessageRepositoryInterface):
        self._message_repository = message_repository

    async def get_messages_for_graph(self, start_date: datetime.date, finish_date: datetime.date):
        return await self._message_repository.get_messages_for_graph(start_date, finish_date)
