from flask_restful import Resource, request
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

        post = PostModel.objects.get(id=values["post_id"], deleted_at=None)
        if not post:
            return {"error": "Post not found."}, 404

        created_comment = CommentModel(
            author=request.user["id"],
            post_id=values["post_id"],
            content=values["content"],
        ).save()

        post.comments.append(created_comment.id)
        post.save()
        return {"message": "Comment successfully created."}, 201
