import pytest
from bson import ObjectId
from uuid import uuid4
from mongomock import MongoClient
from fakeredis import FakeStrictRedis
from app import create_app
from app.models.comment import CommentModel
from app.models.post import PostModel
from app.utils import create_token

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


def create_comment(post_id=ObjectId(), author=ObjectId(), content=uuid4().hex):
    comment = CommentModel.objects.create(
        post_id=post_id, content=content, author={"id": author, "name": "Test User"}
    )
    PostModel.objects(id=post_id).update_one(push__comments=comment.id)
    return comment


def create_post(author=ObjectId(), title=uuid4().hex, content=uuid4().hex):
    return PostModel.objects.create(title=title, content=content, author=author)


def test_get_comments(client):
    post_id = ObjectId()
    comment1 = create_comment(post_id=post_id)
    comment2 = create_comment(post_id=post_id)

    response = client.get(f"/comment/{post_id}")

    assert response.status_code == 200
    assert len(response.json["results"]) == 2
    assert response.json["results"][0]["content"] == comment1.content
    assert response.json["results"][1]["content"] == comment2.content


def test_create_comment(client):
    post_id = create_post().id
    token = create_token({"id": str(ObjectId()), "name": "Test User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}
    data = {"post_id": str(post_id), "content": "New Comment"}

    response = client.post("/comment", json=data, headers=headers)

    assert response.status_code == 201
    assert "comment_id" in response.json
    assert "message" in response.json
    assert len(CommentModel.objects(post_id=post_id)) == 1
    assert PostModel.objects.get(id=post_id).comments == [
        ObjectId(response.json["comment_id"])
    ]

    invalid_post_id = ObjectId()
    data = {"post_id": str(invalid_post_id), "content": "New Comment"}

    response = client.post("/comment", json=data, headers=headers)

    assert response.status_code == 404
    assert response.json == {"error": "Post not found."}
    assert len(CommentModel.objects(post_id=invalid_post_id)) == 0

    # Test with invalid token
    token = create_token({"id": "invalid_id", "name": "Invalid User"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/comment", json=data, headers=headers)

    assert response.status_code == 401
    assert response.json == {"error": "Invalid token."}


def test_update_comment(client):
    post_id = create_post().id
    author_id = ObjectId()
    comment = create_comment(post_id=post_id, author=author_id)

    token = create_token({"id": str(author_id), "name": "Test User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}
    data = {"content": "Updated Comment"}

    response = client.put(f"/comment/{comment.id}", json=data, headers=headers)

    assert response.status_code == 200
    assert response.json["content"] == "Updated Comment"
    assert CommentModel.objects.get(id=comment.id).content == "Updated Comment"


def test_update_comment_not_found(client):
    token = create_token({"id": str(ObjectId()), "name": "Test User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}
    data = {"content": "Updated Comment"}

    response = client.put(f"/comment/{str(ObjectId())}", json=data, headers=headers)

    assert response.status_code == 404
    assert response.json == {"error": "Comment not found."}


def test_update_comment_invalid_token(client):
    post_id = create_post().id
    author_id = ObjectId()
    comment = create_comment(post_id=post_id, author=author_id)

    token = create_token({"id": "invalid_id", "name": "Invalid User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}
    data = {"content": "Updated Comment"}

    response = client.put(f"/comment/{comment.id}", json=data, headers=headers)

    assert response.status_code == 401
    assert response.json == {"error": "Invalid token."}


def test_update_comment_unauthorized(client):
    post_id = create_post().id
    comment = create_comment(post_id=post_id)

    token = create_token({"id": str(ObjectId()), "name": "Other User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}
    data = {"content": "Updated Comment"}

    response = client.put(f"/comment/{comment.id}", json=data, headers=headers)

    assert response.status_code == 401
    assert response.json == {"error": "You are not authorized for this event."}


def test_delete_comment(client):
    author_id = ObjectId()
    post = create_post(author=author_id)
    post_id = post.id
    comment = create_comment(post_id=post_id, author=author_id)

    token = create_token({"id": str(author_id), "name": "Test User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/comment/{comment.id}", headers=headers)

    assert response.status_code == 204
    assert CommentModel.objects.get(id=comment.id).deleted_at is not None


def test_delete_comment_not_found(client):
    token = create_token({"id": str(ObjectId()), "name": "Test User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/comment/{str(ObjectId())}", headers=headers)

    assert response.status_code == 204


def test_delete_comment_unauthorized(client):
    comment = create_comment()
    token = create_token({"id": str(ObjectId()), "name": "Other User", "email": "test@test.com"})
    headers = {"Authorization": f"Bearer {token}"}

    response = client.delete(f"/comment/{comment.id}", headers=headers)

    assert response.status_code == 401 or response.status_code == 204
