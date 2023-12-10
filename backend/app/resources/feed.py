from flask_restful import Resource, request
from app.models.post import PostModel
from app.schemas.post import post_schema, PostSchema
from app.utils import paginate_query


class FeedResource(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 50, type=int)
        sort_vote = request.args.get("vote", None, type=str)
        sort_date = request.args.get("date", "desc", type=str)

        sort_values = []

        if sort_vote:
            if sort_vote.lower() == "asc":
                sort_values.append("vote")
            else:
                sort_values.append("-vote")
        if sort_date.lower() == "asc":
            sort_values.append("created_at")
        else:
            sort_values.append("-created_at")

        query = PostModel.objects(deleted_at=None)

        return paginate_query(
            query, page, limit, PostSchema(exclude=["comments"]), sort_values
        )
