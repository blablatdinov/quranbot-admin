from http import HTTPStatus

import pytest
from django.test import Client

pytestmark = [pytest.mark.django_db]


def test_main_page(client: Client, main_heading: str) -> None:
    response = client.get('/index')

    assert response.status_code == HTTPStatus.OK
    assert main_heading in str(response.content)


def test_landing_page(anon: Client, main_heading: str) -> None:
    response = anon.get('/')

    assert response.status_code == HTTPStatus.OK
    assert main_heading in str(response.content)
