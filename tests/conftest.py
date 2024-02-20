"""
This module is used to provide configuration, fixtures, and plugins for pytest.

It may be also used for extending doctest's context:
1. https://docs.python.org/3/library/doctest.html
2. https://docs.pytest.org/en/latest/doctest.html
"""

import pytest
from mixer.backend.django import mixer as mixer_

pytest_plugins = [
    # Should be the first custom one:
    'plugins.django_settings',
    # TODO: add your own plugins here!
    'plugins.main.main_templates',
]


@pytest.fixture()
def mixer():
    return mixer_
