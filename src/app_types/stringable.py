class Stringable(object):
    """Интерфейс классов, приводимых к строке."""

    def __str__(self):
        """Строковое представление.

        :raises NotImplementedError: if not implemented
        """
        raise NotImplementedError
