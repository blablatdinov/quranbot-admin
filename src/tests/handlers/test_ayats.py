import pytest


@pytest.fixture
async def ayats(test_db_connection):
    query = """
        INSERT INTO content_sura
        (ayat_id, number, pars_hash, link, child_elements_count)
        VALUES
        (1, 1, 'hash', 'link', 1);

        INSERT INTO content_file
        (ayat_id, link_to_file, tg_file_id, name)
        VALUES
        (1, 'link', 'file_id', 'name');

        INSERT INTO content_morningcontent
        (ayat_id, additional_content, day)
        VALUES
        (1, 'content', 1);

        INSERT INTO content_ayat
        (additional_content, arab_text, trans, sura_id, ayat, html, audio_id, one_day_content_id, content)
        VALUES
        ('additional', 'arab', 'transliteration', 1, '1-7', '<html></html>', 1, 1, 'content')
    """
    await test_db_connection.execute(query)


@pytest.mark.slow
def test_get_ayats(client):
    got = client.get('/api/v1/ayats')
    payload = got.json()['results']

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert list(payload[0].keys()) == ['ayat_id', 'mailing_day']


@pytest.mark.slow
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
