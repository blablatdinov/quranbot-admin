import pytest

from repositories.ayat import AyatDetailQuery, AyatRepository


@pytest.mark.xfail
async def test(db_session):
    ayat = await AyatRepository(AyatDetailQuery(), db_session).get_ayat_detail(1)

    assert ayat.id == 1
