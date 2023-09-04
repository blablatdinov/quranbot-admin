def test(pgsql, client):
    got = client.get('/api/v1/ayats')

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert len(got.json()['results']) == 50
    assert list(got.json()['results'][0].keys()) == [
        'id',
        'content',
        'arab_text',
        'trans',
        'sura_num',
        'ayat_num',
        'audio_file_link',
    ]
