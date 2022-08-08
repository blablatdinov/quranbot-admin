from pathlib import Path

import pytest

from repositories.ayat import AyatDetailQuery, AyatRepository
from settings import settings


@pytest.fixture()
async def ayats(db_session):
    dump_file = Path(settings.BASE_DIR / 'tests' / 'fixtures' / 'ayats_dump.sql')
    queries = dump_file.read_text().split(';')
    for query in queries:
        await db_session.execute(query.strip())


async def test(db_session, ayats):
    ayat = await AyatRepository(AyatDetailQuery(), db_session).get_ayat_detail(1)

    assert ayat.id == 1
