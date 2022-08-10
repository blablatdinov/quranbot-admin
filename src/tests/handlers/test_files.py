import pytest

from main import app
from repositories.file import FileRepository, FileRepositoryInterface


@pytest.fixture()
def file():
    return b''


class FileRepositoryMock(FileRepositoryInterface):

    async def create(self, filename):
        pass


@pytest.fixture(autouse=True)
def override_deps():
    app.dependency_overrides[FileRepository] = FileRepositoryMock


@pytest.mark.usefixtures('override_queue_dep')
def test(client, file):
    got = client.post('/api/v1/files/', files={'file': file})

    assert got.status_code == 201
