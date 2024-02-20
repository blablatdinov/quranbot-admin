from http import HTTPStatus

import pytest
from django.test import Client


@pytest.mark.django_db()
def test_health_check(client: Client) -> None:
    """This test ensures that health check is accessible."""
    response = client.get('/health/')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'page',
    [
        '/robots.txt',
        '/humans.txt',
    ],
)
def test_specials_txt(client: Client, page: str) -> None:
    """This test ensures that special `txt` files are accessible."""
    response = client.get(page)

    assert response.status_code == HTTPStatus.OK
    assert response.get('Content-Type') == 'text/plain'
