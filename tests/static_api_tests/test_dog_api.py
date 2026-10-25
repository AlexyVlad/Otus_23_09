import pytest
import requests

BASE_URL = "https://dog.ceo/api"


def test_get_all_breeds():
    response = requests.get(
        f"{BASE_URL}/breeds/list/all", timeout=15
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], dict)
    assert "retriever" in data["message"]


def test_get_random_dog_image():
    response = requests.get(
        f"{BASE_URL}/breeds/image/random", timeout=15
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["message"].startswith(
        "https://images.dog.ceo/"
    )


@pytest.mark.parametrize(
    "breed",
    ["hound", "beagle", "retriever"],
)
def test_get_random_image_by_breed(breed):
    response = requests.get(
        f"{BASE_URL}/breed/{breed}/images/random",
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["message"].startswith(
        "https://images.dog.ceo/"
    )


@pytest.mark.parametrize(
    "breed",
    ["hound", "poodle"],
)
def test_get_sub_breeds(breed):
    response = requests.get(
        f"{BASE_URL}/breed/{breed}/list", timeout=15
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], list)


def test_get_multiple_random_images():
    response = requests.get(
        f"{BASE_URL}/breeds/image/random/3",
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["message"], list)
    assert len(data["message"]) == 3