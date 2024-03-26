from app.models.tag import TagModel
from app.models.user import UserModel
from app.schemas.user import user_schema
from app import create_app
from app.utils import create_token
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
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
    return user_schema.dump(user)


def test_tag_resource_post(client):
    user = create_user()
    token = create_token(user)

    values = {"name": "Test Tag"}

    response = client.post(
        "/tag",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    assert "id" in response.json
    assert "name" in response.json
    assert "message" in response.json
    assert response.json["message"] == "Tag successfully created."


def test_tag_resource_post_existing_tag(client):
    user = create_user()
    token = create_token(user)

    tag_name = "Existing Tag"
    values = {"name": tag_name}
    client.post(
        "/tag",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )
    response = client.post(
        "/tag",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 409
    assert "id" in response.json
    assert "name" in response.json
    assert "message" in response.json
    assert response.json["message"] == "This tag already exists."


def test_tag_resource_post_unallowed_attribute(client):
    user = create_user()
    token = create_token(user)

    values = {"name": "Test Tag", "extra_attribute": "Extra"}

    response = client.post(
        "/tag",
        json=values,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Unallowed attribute."
