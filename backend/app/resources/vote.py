from flask_restful import Resource, request
from app.models.vote import VoteModel
from app.models.post import PostModel
from app.schemas.vote import vote_schema
from app.middleware.auth import auth_required


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
        # NOTE(ahmet): I definitely know this block could be more better...
        values = request.get_json()
        errors = vote_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        if values["vote_value"] > 1 or values["vote_value"] < -1:
            return {"error": "Unallowed attribute."}, 400

        post = PostModel.objects(id=values["post_id"], deleted_at=None).first()
        if not post:
            return {"error": "Post not found."}, 404

        recent_vote = VoteModel(author=request.user["id"], post_id=values["post_id"])

        if recent_vote:
            if values["vote_value"] == 0:
                if recent_vote.vote_value == -1:
                    post.vote += 1
                elif recent_vote.vote_value == 1:
                    post.vote -= 1

                recent_vote.delete()
                post.save()
                return {"message": "Vote saved successfully."}, 201

            if recent_vote.vote_value == values["vote_value"]:
                return {"message": "Vote saved successfully."}, 201

            recent_vote.vote_value = values["vote_value"]
            recent_vote.save()
            if post.vote + recent_vote.vote_value == 0:
                post.vote = recent_vote.vote_value
            else:
                post.vote += recent_vote.vote_value
            post.save()
            return {"message": "Vote saved successfully."}, 201

        if values["vote_value"] == 0:
            return {"error": "You cannot cast a blank vote."}, 400

        VoteModel(
            author=request.user["id"],
            post_id=values["post_id"],
            vote_value=values["vote_value"],
        ).save()
        post.vote += values["vote_value"]
        post.save()
        return {"message": "Vote saved successfully."}, 201
