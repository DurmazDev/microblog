from flask_restful import Resource, request
from bson import ObjectId
from app.utils import decode_token
from app.models.post import PostModel
from app.models.user import UserModel
from app.models.comment import CommentModel
from app.models.vote import VoteModel
from app.models.tag import TagModel
from app.schemas.post import post_schema, PostSchema
from app.schemas.comment import comment_schema
from app.schemas.tag import tag_schema
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
        comments = CommentModel.objects.filter(
            id__in=post.comments, deleted_at=None
        ).limit(50)
        comments = comment_schema.dump(comments, many=True)

        if not comments:
            comments = []

        if post.tags != None:
            tags = TagModel.objects.filter(id__in=post.tags, deleted_at=None).limit(10)
            tags = tag_schema.dump(tags, many=True)

            if not tags:
                tags = []
            else:
                post.tags = tags

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
                return {"error": "Invalid token."}, 401

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
        excluded_fields = ["content", "comments", "vote", "tags"]
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
            return {"error": "Post not found"}, 404
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


class PostTagsView(Resource):
    """
    This view handles the tags associated with a post.

    Endpoint:
        GET /posts/<id>/tag
        POST /posts/<id>/tag
        DELETE /posts/<id>/tag
    """

    def get(self, id):
        """
        Retrieves tags associated with a post.

        Parameters:
            id (str): Post ID

        Returns:
            JSON: List of tags associated with the post.
        """
        try:
            post = PostModel.objects(id=id, deleted_at=None).get()
            if post.tags == None:
                return {"error": "No tags found."}, 404
        except PostModel.DoesNotExist:
            return {"error": "Post not found"}, 404

        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("limit", default=10, type=int)
        start_index = (page - 1) * per_page

        tags = (
            TagModel.objects.filter(id__in=post.tags, deleted_at=None)
            .skip(start_index)
            .limit(per_page)
        )
        return tag_schema.dump(tags, many=True)

    @auth_required
    def post(self, id):
        """
        Adds a new tag to a post.

        Parameters:
            id (str): Post ID

        Returns:
            JSON: Message indicating successful tag addition or error message
        """
        params = request.get_json()
        try:
            if params["id"] != None and ObjectId.is_valid(params["id"]):
                tag_id = params["id"]
            else:
                return {"error": "No tag found with this id."}, 400
        except KeyError:
            return {"error": "id field is required."}, 400

        try:
            post = PostModel.objects(
                id=id, author=request.user["id"], deleted_at=None
            ).get()
        except PostModel.DoesNotExist:
            return {"error": "Post not found"}, 404

        try:
            tag = TagModel.objects(id=tag_id, deleted_at=None).get()
        except TagModel.DoesNotExist:
            return {"error": "Tag not found"}, 404

        for item in post.tags:
            if item == tag.id:
                return {"error": "Tag already exists."}, 400
        post.tags.append(tag["id"])
        post.save()
        return {"message": "Tag added successfully."}, 201

    @auth_required
    def delete(self, id):
        """
        Removes a tag from a post.

        Parameters:
            id (str): Post ID

        Returns:
            JSON: Message indicating successful tag removal or error message
        """
        params = request.get_json()
        try:
            if params["id"] != None and ObjectId.is_valid(params["id"]):
                tag_id = ObjectId(params["id"])
            else:
                return {"error": "No tag found with this id."}, 400
        except KeyError:
            return {"error": "id field is required."}, 400

        try:
            post = PostModel.objects(
                id=id, author=request.user["id"], deleted_at=None
            ).get()
        except PostModel.DoesNotExist:
            return {"error": "Post not found"}, 404

        if post.tags == None:
            return {"error": "No tags found."}, 404
        else:
            if ObjectId(tag_id) in post.tags:
                post.tags.remove(ObjectId(tag_id))
                post.save()
                return {"message": "Tag removed successfully."}, 204
            else:
                return {"error": "No tag found with this id in post tags."}, 404
