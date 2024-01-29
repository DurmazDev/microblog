from flask_restful import Resource, request
from bson import ObjectId
from app.utils import decode_token
from app.models.post import PostModel
from app.schemas.post import post_schema, PostSchema
from app.models.user import UserModel
from app.models.comment import CommentModel
from app.schemas.comment import comment_schema
from app.models.vote import VoteModel
from app.config import FRONTEND_ROOT
from app.middleware.auth import auth_required
from jwt import PyJWTError


class ShowPostResource(Resource):
    """
    Endpoint:
        GET /posts/<id>

    Parameters:
        id (str): Post ID or URL slug.

    Returns:
        JSON: Post details, including associated comments.
    """

    def get(self, id):
        try:
            if ObjectId.is_valid(id):
                post = PostModel.objects(id=id, deleted_at=None).get()

            else:
                url = (
                    "http://" + FRONTEND_ROOT + "/post/" + id
                )  # WARN(ahmet): in prod, we need more s'es, (https)
                post = PostModel.objects(url=url, deleted_at=None).get()
        except PostModel.DoesNotExist:
            return {"error": "Post not found"}, 404
        comments = CommentModel.objects.filter(id__in=post.comments)
        comments = comment_schema.dump(comments, many=True)

        if not comments:
            comments = []

        try:
            author = UserModel.objects(id=post.author, deleted_at=None).get()
        except UserModel.DoesNotExist:
            author = {"id": None, "name": "Deleted User"}
            pass

        if request.headers.get("Authorization"):
            try:
                decoded_token = decode_token(
                    request.headers.get("Authorization").split(" ")[-1]
                )
                recent_vote = VoteModel.objects(
                    author=decoded_token["id"], post_id=post.id
                ).get()
                if recent_vote:
                    setattr(author, "vote", recent_vote.vote_value)
            except VoteModel.DoesNotExist:
                pass
            except PyJWTError:
                return {"error": "Invalid token"}, 401

        post.author = author
        post.comments = comments
        return post_schema.dump(post)


class PostResource(Resource):
    """
    Endpoint:
        GET /posts
        POST /posts
        PUT /posts/<id>
        DELETE /posts/<id>
    """

    @auth_required
    def get(self):
        """
        Retrieves posts authored by the authenticated user.

        Returns:
            JSON: List of user's posts.
        """
        excluded_fields = ["content", "comments", "vote"]
        posts = (
            PostModel.objects.filter(author=request.user["id"], deleted_at=None)
            .order_by("-updated_at")
            .exclude(*excluded_fields)
        )

        if not posts:
            return {"error": "No post found."}, 404
        for obj in posts:
            obj.author = {"id": request.user["id"], "name": request.user["name"]}
        return PostSchema(exclude=excluded_fields).dump(posts, many=True)

    @auth_required
    def post(self):
        """
        Creates a new post for the authenticated user.

        Returns:
            JSON: Message indicating successful post creation and post details.
        """
        values = request.get_json()
        errors = post_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        created_post = PostModel(
            title=values["title"],
            author=request.user["id"],
            content=values["content"],
        ).save()

        return {
            "message": "Post created successfully.",
            "post_id": str(created_post.id),
            "url": str(created_post.url),
        }, 201

    @auth_required
    def put(self, id):
        """
        Updates an existing post authored by the authenticated user.

        Parameters:
            id (str): Post ID

        Returns:
            JSON: Updated post details, including associated comments.
        """
        values = request.get_json()
        data = post_schema.load(values)
        try:
            post = PostModel.objects(id=id, deleted_at=None).get()
        except PostModel.DoesNotExist:
            return {"error": "User not found"}, 404
        if ObjectId(request.user["id"]) != post.author:
            return {"error": "You are not authorized for this event."}, 401

        for key, value in data.items():
            setattr(post, key, value)
        post.save()

        comments = CommentModel.objects.filter(id__in=post.comments).limit(50)
        comments = comment_schema.dump(comments, many=True)
        post.comments = comments

        return post_schema.dump(post)

    @auth_required
    def delete(self, id):
        """
        Deletes an existing post authored by the authenticated user.

        Parameters:
            id (str): Post ID

        Returns:
            int: HTTP status code 204 for successful deletion.
        """
        try:
            authenticated_user = UserModel.objects(
                id=request.user["id"], deleted_at=None
            ).get()
        except UserModel.DoesNotExist:
            return {"error": "You are not authorized for this event."}, 401

        try:
            post = PostModel.objects(id=id, deleted_at=None).get()
        except PostModel.DoesNotExist:
            return {"error": "Post not found"}, 404
        if post.author != authenticated_user.id:
            return {"error": "You are not authorized for this event."}, 401

        post.soft_delete()
        return {}, 204
