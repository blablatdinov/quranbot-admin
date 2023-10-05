from pathlib import Path


def test(pgsql, client):
    got = client.get('/api/v1/files/')

    assert got.status_code == 200
    assert list(got.json().keys()) == ['count', 'next', 'prev', 'results']
    assert len(got.json()['results']) == 50
    assert list(
        got.json()['results'][0].keys(),
    ) == [
        'id',
        'link',
        'telegram_file_id',
        'name',
    ]


async def test_create_file(pgsql, client, freezer, wait_event):
    freezer.move_to('2023-09-05')
    got = client.post('/api/v1/files/', files={
        'file': ('empty.mp3', Path('src/tests/fixtures/empty.mp3').read_bytes()),
    })
    published_event = wait_event('File.SendTriggered', 1)
    updated_db_row = await pgsql.fetch_one(
        'select * from files where file_id = :file_id',
        {'file_id': published_event['data']['file_id']},
    )

    assert got.status_code == 201, got.content
    assert published_event['data']['source'] == 'disk'
    assert 'media/empty.mp3' in published_event['data']['path']
    assert Path(
        published_event['data']['path'],
    ).read_bytes() == Path('src/tests/fixtures/empty.mp3').read_bytes()
    assert updated_db_row['created_at'].strftime('%Y-%m-%dT%H:%M:%S') == '2023-09-05T00:00:00'
