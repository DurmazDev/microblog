from flask_restful import Resource, request
from bson import ObjectId
from app.utils import paginate_query

from app.middleware.auth import auth_required
from app.models.comment import CommentModel, AuthorEmbedded
from app.models.post import PostModel
from app.schemas.comment import comment_schema


class CommentResource(Resource):
    """
    Endpoint:
        GET /comments/<id>
        POST /comments
        PUT /comments/<id>
        DELETE /comments/<id>
    """

    def get(self, id):
        """
        Lists the comments of the post.

        Parameters:
            id (ObjectId): Post ID Value

        Returns:
            JSON: List of comments with pagination as JSON
        """
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 50, type=int)

        query = CommentModel.objects(post_id=id, deleted_at=None)
        return paginate_query(query, page, limit, comment_schema)

    @auth_required
    def post(self):
        """
        Creates a new comment on a post.

        Returns:
            JSON: Message indicating successful comment creation or error message
        """
        values = request.get_json()
        errors = comment_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        post = PostModel.objects(id=values["post_id"], deleted_at=None).first()
        if not post:
            return {"error": "Post not found."}, 404

        created_comment = CommentModel(
            author=AuthorEmbedded(id=request.user["id"], name=request.user["name"]),
            post_id=values["post_id"],
            content=values["content"],
        ).save()

        post.comments.append(created_comment.id)
        post.save()
        return {
            "comment_id": str(created_comment.id),
            "message": "Comment successfully created.",
        }, 201

    @auth_required
    def put(self, id):
        """
        Updates an existing comment.

        Parameters:
            id (ObjectId): Comment ID Value

        Returns:
            JSON: Updated comment as JSON or error message
        """
        values = request.get_json()
        data = comment_schema.load(values)
        comment = CommentModel.objects(id=id, deleted_at=None).first()
        if not comment:
            return {"error": "Comment not found"}, 404
        if comment.author.id != ObjectId(request.user["id"]):
            return {"error": "You are not authorized for this event."}, 401

        for key, value in data.items():
            setattr(comment, key, value)
        comment.save()
        return comment_schema.dump(comment), 200

    @auth_required
    def delete(self, id):
        """
        Deletes a comment.

        Parameters:
            id (ObjectId): Comment ID Value

        Returns:
            int: HTTP status code 204 for successful deletion or error message
        """
        comment = CommentModel.objects(
            id=id, author__id=request.user["id"], deleted_at=None
        ).first()

        post = PostModel.objects(id=comment["post_id"], deleted_at=None).first()
        if not post:
            return {}, 204

        post.comments.remove(comment.id)
        post.save()
        comment.soft_delete()
        return {}, 204
