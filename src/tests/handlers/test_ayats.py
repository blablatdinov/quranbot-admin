from handlers.v1.schemas.ayats import AyatModelShort
from main import app
from repositories.ayat import ElementsCount, ElementsCountInterface
from repositories.paginated_sequence import PaginatedSequence, PaginatedSequenceInterface


class ElementsCountMock(ElementsCountInterface):

    def update_query(self, query: str):
        return self

    async def get(self):
        return 1


class PaginatedSequenceMock(PaginatedSequenceInterface):

    def update_query(self, query: str):
        return self

    def update_model_to_parse(self, model_to_parse):
        return self

    async def get(self):
        return [AyatModelShort(id=1, mailing_day=1)]


app.dependency_overrides[ElementsCount] = ElementsCountMock
app.dependency_overrides[PaginatedSequence] = PaginatedSequenceMock


def test_get_ayats(client_factory):
    got = client_factory(app).get('/api/v1/ayats')
    payload = got.json()['results']

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert list(payload[0].keys()) == ['id', 'mailing_day']


def test_get_ayat_detail(client):
    got = client.get('/api/v1/ayats/1')

    assert got.status_code == 200
    assert list(got.json().keys()) == [
        'ayat_id',
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
