import pytest
from uuid import uuid4
from bson import ObjectId
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
from app import create_app
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


def test_get_user(client):
    response = client.get("/user", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "name" in response.json
    assert "email" in response.json


def test_get_user_not_found(client):
    temp_token = create_token({"id": str(ObjectId())})
    response = client.get("/user", headers={"Authorization": f"Bearer {temp_token}"})

    assert response.status_code == 404
    assert "error" in response.json
    assert response.json["error"] == "User not found."


def test_update_user(client):
    response = client.put(
        f"/user/{user['id']}",
        json={"name": "Updated Name", "email": "updated@example.com"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert "name" in response.json
    assert response.json["name"] == "Updated Name"
    assert "email" in response.json
    assert response.json["email"] == "updated@example.com"


def test_update_user_unauthorized(client):
    response = client.put(
        f"/user/{str(ObjectId())}",
        json={"name": "Updated Name", "email": "updated@example.com"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert "error" in response.json
    assert response.json["error"] == "You are not authorized for this event."


# TODO(ahmet): This test fails because of a bug in deletion code, firstly fix the deletion part of code.
# then write unauthorized_deletion and not_found_deletion tests.
# def test_delete_user(client):
#     response = client.delete("/user", headers={"Authorization": f"Bearer {token}"})

#     assert response.status_code == 202
#     assert "message" in response.json
#     assert (
#         response.json["message"]
#         == "An email sent for delete confirmation, please confirm your deletion from your email."
#     )
