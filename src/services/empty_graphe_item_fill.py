"""Модуль, содержащий класс для заполнения пустых значений для графика.

Classes:
    GraphZeroValueItemSave
"""
import datetime

from handlers.v1.schemas.messages import MessageGraphDataItem
from repositories.messages import MessageRepositoryInterface


class GraphZeroValueItemSave(object):
    """Класс, заполняющий пустые значения в графике."""

    def __init__(self, message_repository: MessageRepositoryInterface):
        """Конструктор класса.

        :param message_repository: MessageRepositoryInterface
        """
        self._message_repository = message_repository

    async def get_messages_for_graph(
        self,
        start_date: datetime.date,
        finish_date: datetime.date,
    ) -> list[MessageGraphDataItem]:
        """Получить данные для графика.

        :param start_date: dateitme.date
        :param finish_date: dateitme.date
        :return: list[MessageGraphDataItem]
        """
        db_query_result = await self._message_repository.get_messages_for_graph(start_date, finish_date)
        while start_date <= finish_date:
            if start_date not in db_query_result:
                db_query_result[start_date] = 0
            start_date += datetime.timedelta(days=1)
        return sorted(
            [
                MessageGraphDataItem(date=date, messages_count=messages_count)
                for date, messages_count in db_query_result.items()
            ],
            key=lambda message_graph_data_item: message_graph_data_item.date,
        )
