from http import HTTPStatus

from django.test import Client


def test_main_page(client: Client, main_heading: str) -> None:
    response = client.get('/index')

    assert response.status_code == HTTPStatus.OK
    assert main_heading in str(response.content)


def test_landing_page(client: Client, main_heading: str) -> None:
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert main_heading in str(response.content)
