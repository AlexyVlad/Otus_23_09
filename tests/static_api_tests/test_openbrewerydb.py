import pytest
import requests

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"


def test_get_breweries():
    response = requests.get(
        BASE_URL,
        params={"per_page": 5},
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

    if data:
        assert "id" in data[0]
        assert "name" in data[0]


@pytest.mark.parametrize("per_page", [1, 3, 5])
def test_breweries_pagination(per_page):
    response = requests.get(
        BASE_URL,
        params={"per_page": per_page},
        timeout=15,
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= per_page


@pytest.mark.parametrize(
    "brewery_type",
    ["micro", "brewpub", "regional"],
)
def test_filter_by_brewery_type(brewery_type):
    response = requests.get(
        BASE_URL,
        params={
            "by_type": brewery_type,
            "per_page": 5,
        },
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for brewery in data:
        assert brewery["brewery_type"] == brewery_type


def test_search_breweries():
    response = requests.get(
        f"{BASE_URL}/search",
        params={"query": "stone"},
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for brewery in data:
        assert isinstance(brewery, dict)
        assert brewery.get("id")
        assert brewery.get("name")


def test_get_random_brewery():
    response = requests.get(
        f"{BASE_URL}/random",
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1

    brewery = data[0]

    assert brewery["id"]
    assert brewery["name"]
    assert brewery["brewery_type"]


def test_get_brewery_by_id():
    response = requests.get(
        BASE_URL,
        params={"per_page": 1},
        timeout=15,
    )

    assert response.status_code == 200
    breweries = response.json()
    assert breweries

    brewery_id = breweries[0]["id"]

    details_response = requests.get(
        f"{BASE_URL}/{brewery_id}",
        timeout=15,
    )

    assert details_response.status_code == 200
    assert details_response.json()["id"] == brewery_id
