import pytest
from uuid import uuid4
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
from bcrypt import hashpw, gensalt
from app import create_app
from app.models.post import PostModel
from app.models.comment import CommentModel
from app.models.user import UserModel
from app.schemas.user import user_schema

mongo_client = MongoClient()
redis_client = FakeStrictRedis()

app = create_app(
    db="mongoenginetest",
    mongodb_uri="mongodb://localhost",
    mongo_client_class=MongoClient,
    redis_client=redis_client,
    TESTING=True,
)
TEST_HASHED_PASSWORD = hashpw("testpass".encode("utf-8"), gensalt(rounds=12))


def create_user():
    user = UserModel(
        name="Test User",
        email=f"{uuid4()}@example.com",
        password=hashpw("test_pass".encode("utf-8"), gensalt(rounds=12)),
    ).save()
    return user_schema.dump(user)


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_feed_no_results(client):
    response = client.get("/feed")

    assert response.status_code == 404
    assert response.json["error"] == "No results found."


def test_get_feed_pagination(client):
    email = f"test_{uuid4()}@example.com"
    user1 = UserModel.objects.create(
        name="Test User 1", email=email, password=TEST_HASHED_PASSWORD
    )
    for i in range(60):
        PostModel.objects.create(
            title=f"Post {i+1}",
            content=f"Content {i+1}",
            author=user1["id"],
        )

    response = client.get("/feed?page=2&limit=50")

    assert response.status_code == 200
    assert response.json["pagination"]["current_page"] == 2
    assert response.json["pagination"]["next_page"] is None
    assert response.json["pagination"]["prev_page"] == 1
    assert response.json["pagination"]["total_count"] == 60
    assert response.json["pagination"]["total_pages"] == 2
    assert len(response.json["results"]) == 10


def test_get_feed(client):
    user1 = create_user()
    # Flush DB
    PostModel.objects().all().delete()

    post1 = PostModel(title="Post 1", content="Content 1", author=user1["id"]).save()
    post2 = PostModel(
        title="Post 2",
        content="Content 2",
        author=user1["id"],
    ).save()
    comment1 = CommentModel(
        post_id=post1.id,
        content="Comment 1",
        author={"id": str(user1["id"]), "name": "Test User"},
    ).save()
    comment2 = CommentModel(
        post_id=post2.id,
        content="Comment 2",
        author={"id": str(user1["id"]), "name": "Test User"},
    ).save()

    post1.comments.append(comment1.id)
    post2.comments.append(comment2.id)

    post1.save()
    post2.save()

    response = client.get("/feed?date=asc")

    assert response.status_code == 200
    assert response.json["results"][0]["url"][:-4] == post1.url[:-4]
    assert response.json["results"][0]["title"] == post1.title
    assert response.json["results"][0]["content"] == post1.content[:200] + "..."
    assert response.json["results"][0]["author"]["id"] == str(user1["id"])
    assert response.json["results"][1]["url"][:-4] == post2.url[:-4]
    assert response.json["results"][1]["title"] == post2.title
    assert response.json["results"][1]["content"] == post2.content[:200] + "..."
    assert response.json["results"][1]["author"]["id"] == str(user1["id"])
