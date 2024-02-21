import pytest
from uuid import uuid4
from bson import ObjectId
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
from app import create_app
from app.models.post import PostModel
from app.models.user import UserModel
from app.schemas.user import user_schema
from app.utils import create_token
from bcrypt import hashpw, gensalt

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


def test_get_posts(client):
    post1 = PostModel.objects.create(
        title="Post 1", content="Content 1", author=user["id"]
    )

    response = client.get("/post", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]["title"] == post1.title


def test_create_post(client):
    response = client.post(
        "/post",
        json={"title": "New Post", "content": "New Content"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert "message" in response.json
    assert "post_id" in response.json
    assert "url" in response.json


def test_update_post(client):
    post = PostModel.objects.create(
        title="Old Title", content="Old Content", author=user["id"]
    )

    response = client.put(
        f"/post/{post.id}",
        json={"title": "New Title", "content": "New Content"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json["title"] == "New Title"
    assert response.json["content"] == "New Content"


def test_unauthorized_post_creation(client):
    response = client.post(
        "/post", json={"title": "New Post", "content": "New Content"}
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Token is missing."

    response = client.post(
        "/post",
        json={"title": "New Post", "content": "New Content"},
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Invalid token."


def test_unauthorized_post_update(client):
    post = PostModel.objects.create(
        title="Old Title", content="Old Content", author=str(ObjectId())
    )

    response = client.put(
        f"/post/{post.id}", json={"title": "New Title", "content": "New Content"}
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Token is missing."

    response = client.put(
        f"/post/{post.id}",
        json={"title": "New Title", "content": "New Content"},
        headers={"Authorization": "Bearer invalid_token"},
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Invalid token."


def test_unauthorized_post_deletion(client):
    post = PostModel.objects.create(
        title="Post to Delete", content="Content to Delete", author=str(ObjectId())
    )
    response = client.delete(f"/post/{post.id}")
    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Token is missing."

    response = client.delete(
        f"/post/{post.id}", headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "Invalid token."


def test_delete_post_not_found(client):
    response = client.delete(
        f"/post/{str(ObjectId())}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "Post not found"


def test_update_post_not_found(client):
    response = client.put(
        f"/post/{str(ObjectId())}",
        json={"title": "New Title", "content": "New Content"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert response
    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "Post not found"


def test_get_post_not_found(client):
    response = client.get(f"/post/{str(ObjectId())}")

    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "Post not found"


def test_delete_post(client):
    post = PostModel.objects.create(
        title="Post to Delete",
        content="Content to Delete",
        author=str(user["id"]),
    )

    response = client.delete(
        f"/post/{post.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204
