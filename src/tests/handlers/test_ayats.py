import pytest
from faker import Faker

from app_types.query import QueryInterface
from handlers.v1.schemas.ayats import AyatModel, AyatModelShort, FileModel
from main import app
from repositories.ayat import AyatRepository, AyatRepositoryInterface
from repositories.paginated_sequence import CachedPaginatedSequence, PaginatedSequence, PaginatedSequenceInterface, ElementsCountInterface, \
    ElementsCount


class ElementsCountMock(ElementsCountInterface):

    def update_query(self, query: str):
        return self

    async def get(self):
        return 1


class PaginatedSequenceMock(PaginatedSequenceInterface):

    def update_query(self, query: QueryInterface):
        return self

    def update_model_to_parse(self, model_to_parse):
        return self

    async def get(self):
        return [AyatModelShort(
            id=1,
            content=self._text(),
            arab_text=self._text(),
            trans=self._text(),
            sura_num=1,
            ayat_num=self._text(),
            audio_file_link=self._text(),
        )]

    def _text(self) -> str:
        return Faker().text(10)


class AyatRepositoryMock(AyatRepositoryInterface):

    async def get_ayat_detail(self, ayat_id: int):
        return AyatModel(
            id=1,
            additional_content='',
            content='',
            arab_text='',
            trans='',
            sura_num=1,
            ayat_num='1-7',
            html='',
            audio_file=FileModel(
                id=1,
                link='',
                telegram_file_id='',
                name=None,
            ),
            mailing_day=1,
        )


@pytest.fixture(autouse=True)
def override_dependency():
    app.dependency_overrides[ElementsCount] = ElementsCountMock
    app.dependency_overrides[PaginatedSequence] = PaginatedSequenceMock
    app.dependency_overrides[AyatRepository] = AyatRepositoryMock
    app.dependency_overrides[CachedPaginatedSequence] = PaginatedSequenceMock


def test_get_ayats(client):
    got = client.get('/api/v1/ayats')
    payload = got.json()['results']

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert list(payload[0].keys()) == [
        'id',
        'content',
        'arab_text',
        'trans',
        'sura_num',
        'ayat_num',
        'audio_file_link',
    ]


def test_get_ayat_detail(client):

    got = client.get('/api/v1/ayats/1')

    assert got.status_code == 200
    assert list(got.json().keys()) == [
        'id',
        'additional_content',
        'content',
        'arab_text',
        'trans',
        'sura_num',
        'ayat_num',
        'html',
        'audio_file',
        'mailing_day',
    ]
