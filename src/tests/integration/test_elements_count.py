from repositories.paginated_sequence import ElementsCount


async def test(db_session):
    elements_count = ElementsCount(db_session)
    elements_count._query = 'SELECT COUNT(*) FROM ayats'  # noqa: WPS437
    got = await elements_count.get()

    assert got == 0
