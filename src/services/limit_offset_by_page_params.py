"""Модуль для трансформации параметров пагинации в параметры для хранилища.

Classes:
    LimitOffset
"""
from typing import final, SupportsInt, TypeAlias

import attrs

PositiveNumber: TypeAlias = SupportsInt


@final
@attrs.define(frozen=True)
class PositiveNum(PositiveNumber):

    _origin: SupportsInt

    def __int__(self):
        if int(self._origin) < 0:
            raise ValueError
        return self._origin


@final
@attrs.define(frozen=True)
class LimitOffset(object):
    """Класс, расчитывающий лимит/отступ для SQL запросов по параметрам пагинации."""

    _page_num: PositiveNumber
    _page_size: PositiveNumber

    @classmethod
    def int_ctor(cls, page_num, page_size):
        return cls(
            PositiveNum(page_num),
            PositiveNum(page_size),
        )

    def offset(self) -> int:
        return (int(self._page_num) - 1) * int(self._page_size)

    def limit(self) -> int:
        return int(self._page_size)
