from app.models.vote import VoteModel
from app.models.post import PostModel
from bson import ObjectId
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
from app import create_app
from app.models.user import UserModel
from app.schemas.user import user_schema
from app.utils import create_token
from bcrypt import hashpw, gensalt
from uuid import uuid4
import pytest

# Mock MongoDB and Redis connections
mongo_client = MongoClient()
redis_client = FakeStrictRedis()

app = create_app(
    db="mongoenginetest",
    mongodb_uri="mongodb://localhost",
    mongo_client_class=MongoClient,
    redis_client=redis_client,
    TESTING=True,
)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def create_user():
    user = UserModel(
        name="Test User",
        email=f"{uuid4()}@example.com",
        password=hashpw("test_pass".encode("utf-8"), gensalt(rounds=12)),
    ).save()
    user_data = user_schema.dump(user)
    return user_data


user = create_user()
token = create_token(user)


def test_vote_resource_post(client):
    post = PostModel.objects.create(
        title="Test Post", content="Test Content", author=user["id"]
    )
    values = {"post_id": str(post.id), "vote_value": 1}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert "message" in response.json
    assert response.json["message"] == "Vote saved successfully."


def test_vote_resource_post_unallowed_attribute(client):
    values = {"post_id": str(ObjectId()), "vote_value": 1, "extra_attribute": "Extra"}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Unallowed attribute."


def test_vote_resource_post_unallowed_vote_value(client):
    post = PostModel.objects.create(
        title="Test Post", content="Test Content", author=user["id"]
    )
    values = {"post_id": str(post.id), "vote_value": 2}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Unallowed vote value."


def test_vote_resource_post_post_not_found(client):
    values = {"post_id": str(ObjectId()), "vote_value": 1}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "Post not found."


def test_vote_resource_post_already_voted(client):
    post = PostModel.objects.create(
        title="Test Post", content="Test Content", author=user["id"]
    )
    VoteModel(author=user["id"], post_id=str(post.id), vote_value=1).save()

    values = {"post_id": str(post.id), "vote_value": 1}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 202
    assert "message" in response.json
    assert response.json["message"] == "You have already voted for this."


def test_vote_resource_post_blank_vote(client):
    post = PostModel.objects.create(
        title="Test Post", content="Test Content", author=user["id"]
    )
    values = {"post_id": str(post.id), "vote_value": 0}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "You cannot cast a blank vote."


def test_vote_resource_post_success(client):
    post = PostModel.objects.create(
        title="Test Post", content="Test Content", author=user["id"]
    )
    values = {"post_id": str(post.id), "vote_value": 1}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert "message" in response.json
    assert response.json["message"] == "Vote saved successfully."


def test_two_users_vote_and_check_vote_value(client):
    def assert_vote_creation(response):
        assert response.status_code == 201
        assert "message" in response.json
        assert response.json["message"] == "Vote saved successfully."

    user1 = create_user()
    user2 = create_user()
    token1 = create_token(user1)
    token2 = create_token(user2)
    post = PostModel.objects.create(
        title="Test Post", content="Test Content", author=user1["id"]
    )
    values = {"post_id": str(post.id), "vote_value": 1}

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token1}"},
    )

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert_vote_creation(response)

    response = client.get(f"/post/{str(post.id)}")

    assert response.status_code == 200
    assert "vote" in response.json
    assert response.json["vote"] == 2

    values = {"post_id": str(post.id), "vote_value": -1}
    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token2}"},
    )

    assert_vote_creation(response)

    response = client.get(f"/post/{str(post.id)}")

    assert response.status_code == 200
    assert "vote" in response.json
    assert response.json["vote"] == 0

    response = client.post(
        "/vote",
        json=values,
        headers={"Authorization": f"Bearer {token1}"},
    )

    assert_vote_creation(response)

    response = client.get(f"/post/{str(post.id)}")

    assert response.status_code == 200
    assert "vote" in response.json
    assert response.json["vote"] == -2
