import pytest
from django.test.client import Client

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def baker():
    from model_bakery import baker as _baker  # noqa: PLC0415

    return _baker
