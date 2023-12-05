from flask_restful import Resource, request
from bson import ObjectId
from app.models.post import PostModel
from app.schemas.post import post_schema, PostSchema
from app.config import DOMAIN_ROOT
from app.middleware.auth import auth_required


class PostResource(Resource):
    @auth_required
    def get(self):
        excluded_fields = ["content", "comments", "vote"]
        posts = PostModel.get_user_posts(
            user_id=request.user["id"], excluded_fields=excluded_fields
        )
        if not posts:
            return {"error": "No post found."}, 404
        return PostSchema(exclude=excluded_fields).dump(posts, many=True)

    def get(self, id):
        if ObjectId.is_valid(id):
            post = PostModel.get_by_id(post_id=id)
        else:
            url = (
                "http://" + DOMAIN_ROOT + "/post/" + id
            )  # WARN(ahmet): in prod, we need more s'es, (https)
            post = PostModel.get_by_url(url=url)
        if not post:
            return {"error": "Post not found."}, 404
        return post_schema.dump(post)

    @auth_required
    def post(self):
        values = request.get_json()
        errors = post_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        created_post = PostModel.create(
            title=values["title"],
            author_id=request.user["id"],
            content=values["content"],
        )
        return {
            "message": "Post created successfully.",
            "post_id": str(created_post.id),
            "url": str(created_post.url),
        }, 201

    @auth_required
    def put(self, id):
        values = request.get_json()
        data = post_schema.load(values)
        post = PostModel.get_by_id(user_id=id)
        if not post:
            return {"error": "User not found"}, 404
        if post.author != request.user["id"]:
            return {"error": "You are not authorized for this event."}, 201
        updated_post = PostModel.update(user_id=id, update_values=data)
        if updated_post:
            return post_schema.dump(updated_post)

        return {"error": "Post not found."}, 404

    @auth_required
    def delete(self, id):
        post = PostModel.get_by_id(user_id=id)
        if not post:
            return {"error": "User not found"}, 404

        post.soft_delete()
        return 204
