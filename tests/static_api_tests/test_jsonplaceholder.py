import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_all_posts():
    response = requests.get(
        f"{BASE_URL}/posts", timeout=15
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100

    if data:
        assert "userId" in data[0]
        assert "id" in data[0]
        assert "title" in data[0]
        assert "body" in data[0]


@pytest.mark.parametrize("post_id", [1, 10, 100])
def test_get_post_by_id(post_id):
    response = requests.get(
        f"{BASE_URL}/posts/{post_id}",
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == post_id
    assert isinstance(data["title"], str)
    assert isinstance(data["body"], str)


def test_get_all_users():
    response = requests.get(
        f"{BASE_URL}/users", timeout=15
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 10

    user = data[0]
    assert "id" in user
    assert "name" in user
    assert "email" in user


@pytest.mark.parametrize("user_id", [1, 3, 5])
def test_filter_posts_by_user(user_id):
    response = requests.get(
        f"{BASE_URL}/posts",
        params={"userId": user_id},
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)

    for post in data:
        assert post["userId"] == user_id


def test_get_comments_for_post():
    response = requests.get(
        f"{BASE_URL}/posts/1/comments",
        timeout=15,
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 5

    for comment in data:
        assert comment["postId"] == 1
        assert "email" in comment
        assert "body" in comment


def test_create_post():
    payload = {
        "title": "API testing",
        "body": "Testing with pytest",
        "userId": 1,
    }

    response = requests.post(
        f"{BASE_URL}/posts",
        json=payload,
        timeout=15,
    )

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]
    assert "id" in data