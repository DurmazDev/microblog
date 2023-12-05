from flask_restful import Resource, request
from bson import ObjectId
from app.middleware.auth import auth_required

from app.models.comment import CommentModel
from app.models.post import PostModel
from app.schemas.comment import comment_schema


class CommentResource(Resource):
    @auth_required
    def post(self):
        values = request.get_json()
        errors = comment_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        post = PostModel.get_by_id(post_id=values["post_id"])
        if not post:
            return {"error": "Post not found."}, 404

        created_comment = CommentModel.create_comment(
            post_id=values["post_id"],
            author=request.user["id"],
            content=values["content"],
        )

        post.comments.append(created_comment.id)
        post.save()
        return {"message": "Comment successfully created."}, 201
