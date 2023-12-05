import httpx


def test():
    got = httpx.get('http://localhost:8080/health')

    assert got.status_code == 200
    assert got.text == 'ok'
