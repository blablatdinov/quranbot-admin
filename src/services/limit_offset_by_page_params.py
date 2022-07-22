class LimitOffsetByPageParams(object):

    _page_num: int
    _page_size: int

    def __init__(self, page_num: int, page_size: int):
        self._page_num = page_num
        self._page_size = page_size

    def calculate(self) -> tuple[int, int]:
        return (
            self._page_size,
            (self._page_num - 1) * self._page_size,
        )
