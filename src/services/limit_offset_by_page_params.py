"""Модуль для трансформации параметров пагинации в параметры для хранилища.

Classes:
    LimitOffset
"""
from typing import SupportsInt, TypeAlias, final

import attrs

PositiveNumber: TypeAlias = SupportsInt


@final
@attrs.define(frozen=True)
class PositiveNum(PositiveNumber):
    """Положительное число."""

    _origin: SupportsInt

    def __int__(self) -> int:
        """Числовое представление.

        :return: int
        :raises ValueError: при отрицательном числе
        """
        if int(self._origin) < 0:
            raise ValueError
        return int(self._origin)


@final
@attrs.define(frozen=True)
class LimitOffset(object):
    """Класс, расчитывающий лимит/отступ для SQL запросов по параметрам пагинации."""

    _page_num: PositiveNumber
    _page_size: PositiveNumber

    @classmethod
    def int_ctor(cls, page_num: int, page_size: int):
        """Конструктор для чисел.

        :param page_num: int
        :param page_size: int
        :return: LimitOffset
        """
        return cls(
            PositiveNum(page_num),
            PositiveNum(page_size),
        )

    def offset(self) -> int:
        """Отступ.

        :return: int
        """
        return (int(self._page_num) - 1) * int(self._page_size)

    def limit(self) -> int:
        """Ограничение.

        :return: int
        """
        return int(self._page_size)
