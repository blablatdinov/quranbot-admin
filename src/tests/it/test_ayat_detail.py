async def test(migrate, client):
    got = client.get('/api/v1/ayats/1/')

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
    assert list(
        got.json()['audio_file'].keys(),
    ) == ['id', 'link', 'telegram_file_id', 'name']
