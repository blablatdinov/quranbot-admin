def test_get_ayats(client):
    got = client.get('/api/v1/ayats')

    assert got.status_code == 200


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
