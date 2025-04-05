import pytest
from django.contrib.auth import get_user_model

pytestmark = [pytest.mark.django_db]

User = get_user_model()


@pytest.fixture(autouse=True)
def user(baker):
    user = baker.make(User, username='hp')
    user.set_password('1')
    user.save()
    return user


def test(client):
    got = client.post(
        '/api/token/',
        data={
            'username': 'hp',
            'password': '1',
        },
    )

    assert got.status_code == 200
