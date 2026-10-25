import requests


def test_url_status_code(url, status_code):
    response = requests.get(
        url,
        timeout=15,
        allow_redirects=True,
    )

    assert response.status_code == status_code