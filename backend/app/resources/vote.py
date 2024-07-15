from flask_restful import Resource, request
from app.models.vote import VoteModel
from app.models.post import PostModel
from app.schemas.vote import vote_schema
from app.middleware.auth import auth_required
from app.utils import create_audit_log


class VoteResource(Resource):
    """
    Resource for managing user votes on posts.

    Endpoint:
        POST /votes

    Returns:
        JSON: Message indicating the success or failure of the vote operation.
    """

    @auth_required
    def post(self):
        """
        Handles POST requests to cast a vote on a post.

        Body:
            {
                "post_id": "string",
                "vote_value": integer in [-1, 0, 1]
            }

        Returns:
            JSON: Message indicating the success or failure of the vote operation.
        """
        values = request.get_json()
        errors = vote_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        if values["vote_value"] > 1 or values["vote_value"] < -1:
            return {"error": "Unallowed vote value."}, 400

        try:
            post = PostModel.objects(id=values["post_id"], deleted_at=None).get()
        except PostModel.DoesNotExist:
            return {"error": "Post not found."}, 404

        try:
            recent_vote = VoteModel.objects(
                author=request.user["id"], post_id=values["post_id"]
            ).get()
            if recent_vote:
                if recent_vote.vote_value == values["vote_value"]:
                    return {"message": "You have already voted for this."}, 202

                post.vote += (-1) * recent_vote.vote_value
                post.vote += values["vote_value"]
                recent_vote.vote_value = values["vote_value"]
                recent_vote.save()
                post.save()
                return {"message": "Vote saved successfully."}, 201
        except VoteModel.DoesNotExist:
            pass

        if values["vote_value"] == 0:
            return {"error": "You cannot cast a blank vote."}, 400

        VoteModel(
            author=request.user["id"],
            post_id=values["post_id"],
            vote_value=values["vote_value"],
        ).save()
        create_audit_log(
            5,
            request.remote_addr,
            request.user_agent,
            f"User {request.user['id']} voted on post {values['post_id']}",
        )
        post.vote += values["vote_value"]
        post.save()
        return {"message": "Vote saved successfully."}, 201
