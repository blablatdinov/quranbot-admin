import pytest


@pytest.fixture
async def ayats(test_db_connection):
    await test_db_connection.execute("""
        INSERT INTO content_sura
        (id, number, pars_hash, link, child_elements_count)
        VALUES 
        (1, 1, 'hash', 'link', 1);
        
        INSERT INTO content_file
        (id, link_to_file, tg_file_id, name) 
        VALUES 
        (1, 'link', 'file_id', 'name');
        
        INSERT INTO content_morningcontent
        (id, additional_content, day)
        VALUES 
        (1, 'content', 1);
        
        INSERT INTO content_ayat
        (additional_content, arab_text, trans, sura_id, ayat, html, audio_id, one_day_content_id, content) 
        VALUES 
        ('additional', 'arab', 'transliteration', 1, '1-7', '<html></html>', 1, 1, 'content')
    """)


def test_get_ayats(client, db, ayats):
    got = client.get('/api/v1/ayats')

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert list(got.json()['results'][0].keys()) == ['id', 'mailing_day']


def test_get_ayat_detail(client, db, ayats):
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
