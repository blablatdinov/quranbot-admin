import pytest


@pytest.fixture()
def main_heading() -> str:
    """An example fixture containing some html fragment."""
    return '<title>Quranbot Admin Panel</title>'
