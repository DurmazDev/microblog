from flask_restful import Resource, request
from bson import ObjectId
from app.models.post import PostModel
from app.schemas.post import post_schema, PostSchema
from app.models.user import UserModel
from app.config import DOMAIN_ROOT, ALLOWED_TAGS, ALLOWED_ATTRIBUTES, DOMAIN_ROOT
from app.middleware.auth import auth_required
import bleach


class ShowPostResource(Resource):
    def get(self, id):
        if ObjectId.is_valid(id):
            post = PostModel.objects.get(id=id, deleted_at=None)
        else:
            url = (
                "http://" + DOMAIN_ROOT + "/post/" + id
            )  # WARN(ahmet): in prod, we need more s'es, (https)
            post = PostModel.objects.get(url=url, deleted_at=None)
        if not post:
            return {"error": "Post not found."}, 404
        return post_schema.dump(post)


class PostResource(Resource):
    @auth_required
    def get(self):
        excluded_fields = ["content", "comments", "vote"]
        posts = (
            PostModel.objects.filter(author=request.user["id"], deleted_at=None)
            .order_by("-updated_at")
            .exclude(*excluded_fields)
        )

        if not posts:
            return {"error": "No post found."}, 404

        return PostSchema(exclude=excluded_fields).dump(posts, many=True)

    @auth_required
    def post(self):
        values = request.get_json()
        errors = post_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        title = bleach.clean(
            values["title"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
        )
        content = bleach.clean(
            values["content"],
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
        )

        created_post = PostModel(
            title=title,
            author_id=request.user["id"],
            content=content,
        ).save()

        return {
            "message": "Post created successfully.",
            "post_id": str(created_post.id),
            "url": str(created_post.url),
        }, 201

    @auth_required
    def put(self, id):
        values = request.get_json()
        data = post_schema.load(values)
        post = PostModel.objects.get(id=id, deleted_at=None)
        if not post:
            return {"error": "User not found"}, 404
        if request.user["id"] != post.author:
            return {"error": "You are not authorized for this event."}, 401

        for key, value in data.items():
            setattr(post, key, value)
        post.save()

        return post_schema.dump(post)

    @auth_required
    def delete(self, id):
        authenticated_user = UserModel.objects.get(
            id=request.user["id"], deleted_at=None
        )
        if not authenticated_user:
            return {"error": "You are not authorized for this event."}, 401

        post = PostModel.objects.get(id=id, deleted_at=None)
        if not post:
            return {"error": "Post not found"}, 404
        if post.author != authenticated_user.id:
            return {"error": "You are not authorized for this event."}, 401

        post.soft_delete()
        return 204
