import pytest
from uuid import uuid4
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
from bcrypt import hashpw, gensalt
from app import create_app
from app.models.user import UserModel
from app.schemas.user import user_schema
from app.utils import create_token

# Mock MongoDB and Redis connections
mongo_client = MongoClient()
redis_client = FakeStrictRedis()
test_pass = "password"
TEST_HASHED_PASSWORD = hashpw(test_pass.encode("utf-8"), gensalt(rounds=12))

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


def test_register_view(client):
    email = f"test_{uuid4()}@example.com"
    data = {"name": "Test User", "email": email, "password": test_pass}
    response = client.post("/auth/register", json=data)

    assert response.status_code == 201

    user = UserModel.objects.get(email=data["email"], deleted_at=None)
    user_data = user_schema.dump(user)

    assert response.json["message"] == "User created successfully."
    assert response.json["user"] == user_data

    # Try with an existing email
    response = client.post("/auth/register", json=data)

    assert response.status_code == 409
    assert response.json == {"error": "User with this e-mail already exists."}


def test_refresh_view(client):
    email = f"test_{uuid4()}@example.com"
    user = UserModel.objects.create(
        name="Test User", email=email, password=TEST_HASHED_PASSWORD
    )
    user_data = user_schema.dump(user)
    token = create_token(user_data)

    response = client.post(
        "/auth/refresh", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "Successfully refreshed token."
    assert response.json["user"]["id"] == user_data["id"]

    response = client.post("/auth/refresh")

    assert response.status_code == 401
    assert response.json == {"error": "Token is missing."}


def test_logout_view(client):
    email = f"test_{uuid4()}@example.com"
    user = UserModel.objects.create(
        name="Test User", email=email, password=TEST_HASHED_PASSWORD
    )
    user_data = user_schema.dump(user)
    token = create_token(user_data)

    response = client.delete(
        "/auth/logout", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 202
    assert response.json == {"message": "Successfully logged out."}
    assert app.config["logout_blocklist"].check_token(user_data["id"], token)

    response = client.delete("/auth/logout")

    assert response.status_code == 401
    assert response.json == {"error": "Token is missing."}


def test_login_view(client):
    email = f"test_{uuid4()}@example.com"
    data = {"name": "Test User", "email": email, "password": test_pass}
    user = UserModel.objects.create(
        name=data["name"],
        email=data["email"],
        password=TEST_HASHED_PASSWORD,
    )
    user_data = user_schema.dump(user)

    response = client.post("/auth/login", json=data)

    assert response.status_code == 200
    assert response.json["message"] == "Successfully logged in."
    assert response.json["user"] == user_data

    data = {"email": email, "password": "wrongpassword"}
    response = client.post("/auth/login", json=data)

    assert response.status_code == 401
    assert response.json == {"error": "Wrong email or password."}

    data = {"email": email, "password": test_pass, "extra": "extra"}
    response = client.post("/auth/login", json=data)

    assert response.status_code == 400
    assert response.json == {"error": "Unallowed attribute."}
