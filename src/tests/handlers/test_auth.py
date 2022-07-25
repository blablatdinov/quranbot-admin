def test_get_token(client):
    got = client.post('/api/v1/auth/', json={
        'username': 'user',
        'password': 'pass',
    })

    assert got.status_code == 201
