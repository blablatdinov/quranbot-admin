import pytest


@pytest.mark.slow
def test_create(client):
    got = client.post('/api/v1/daily-content/', json={
        'day_num': 1,
        'ayat_ids': [1, 2, 3],
    })

    assert got.status_code == 201


@pytest.mark.slow
def test_get_last_daily_content_day(client):
    got = client.get('/api/v1/daily-content/last-registered-day/')

    assert got.status_code == 200
    assert got.json() == {'day_num': 1}
