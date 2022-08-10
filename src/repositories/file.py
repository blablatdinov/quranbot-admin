from app_types.query import QueryInterface

from pypika import Query, Table

from services.limit_offset_by_page_params import LimitOffsetByPageParams


class FilePaginatedQuery(QueryInterface):

    _files_table = Table('content_file')

    def __init__(self, limit_offset_calculator: LimitOffsetByPageParams):
        """Конструктор класса.

        :param limit_offset_calculator: LimitOffsetByPageParams
        """
        self._limit_offset_calculator = limit_offset_calculator

    def query(self):
        """Возвращает запрос.

        :return: str
        """
        limit, offset = self._limit_offset_calculator.calculate()
        return str(
            Query()
            .from_(self._files_table)
            .select(
                self._files_table.id,
                self._files_table.tg_file_id.as_('telegram_file_id'),
                self._files_table.link_to_file.as_('link'),
                self._files_table.name,
            )
            .limit(limit)
            .offset(offset),
        )
