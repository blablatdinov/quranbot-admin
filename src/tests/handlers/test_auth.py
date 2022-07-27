from main import app
from repositories.auth import UserRepository, UserRepositoryInterface, UserSchema
from services.auth import Password, PasswordInterface


class UserRepositoryMock(UserRepositoryInterface):

    storage = [UserSchema(id=1, username='user', password='1')]  # noqa: S106

    async def get_by_username(self, username: str):
        return [user for user in self.storage if user.username == username][0]


class PasswordMock(PasswordInterface):

    async def check(self, username, password):
        return True


app.dependency_overrides[UserRepository] = UserRepositoryMock
app.dependency_overrides[Password] = PasswordMock


def test_get_token(client):
    got = client.post('/api/v1/auth/', data={
        'username': 'user',
        'password': 'pass',
    })

    assert got.status_code == 201
    assert list(got.json().keys()) == ['access_token', 'token_type']
