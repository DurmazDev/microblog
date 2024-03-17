from flask_restful import Resource, request
from app.models.post import PostModel
from app.models.user import UserModel
from app.models.tag import TagModel
from app.schemas.post import post_schema
from bson import ObjectId
from app.models.tag import TagModel


class FeedResource(Resource):
    """
    Endpoint:
        GET /feed

    Query Parameters:
        - page (int, optional): Page number for pagination. Default is 1.
        - limit (int, optional): Number of posts per page. Default is 50.
        - vote (str, optional): Sorting order based on votes. Use 'asc' for ascending and 'desc' for descending.
        - date (str, optional): Sorting order based on creation date. Use 'asc' for ascending and 'desc' for descending.

    Returns:
        A paginated feed of posts based on the specified parameters.
    """

    def get(self):
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 50, type=int)
        sort_vote = request.args.get("vote", None, type=str)
        sort_date = request.args.get("date", "desc", type=str)

        sort_values = []

        if sort_vote:
            if sort_vote.lower() == "asc":
                sort_values.append(("vote", 1))
            else:
                sort_values.append(("vote", -1))
        if sort_date.lower() == "asc":
            sort_values.append(("created_at", 1))
        else:
            sort_values.append(("created_at", -1))

        skip = (page - 1) * limit

        results = (
            PostModel.objects(deleted_at=None)
            .order_by(*[f"{field[0]}_{field[1]}" for field in sort_values])
            .skip(skip)
            .limit(limit)
        )

        author_ids = [post["author"] for post in results]
        author_data = UserModel.objects(id__in=author_ids).only("id", "name")
        author_data_map = {author.id: author.name for author in author_data}

        for post in results:
            author_id = post["author"]
            author_name = author_data_map.get(author_id, "Anonymous")
            post["author"] = {"id": author_id, "name": author_name}

        if hasattr(post, "tags") and post["tags"] is not None:
            tag_ids = post["tags"]
            tag_data = TagModel.objects(id__in=tag_ids, deleted_at=None).only(
                "id", "name"
            )
            tag_data_map = {tag.id: tag for tag in tag_data}

            for i, tag_id in enumerate(tag_ids):
                tag = tag_data_map.get(tag_id)
                if tag is None:
                    tag = {"id": ObjectId(), "name": "Deleted Tag"}
                post["tags"][i] = tag

        total_count = PostModel.objects(deleted_at=None).count()
        total_pages = (total_count + limit - 1) // limit

        if results:
            return {
                "results": post_schema.dump(results, many=True),
                "pagination": {
                    "current_page": page,
                    "next_page": None if page == total_pages else page + 1,
                    "prev_page": None if page == 1 else page - 1,
                    "total_count": total_count,
                    "total_pages": total_pages,
                },
            }, 200
        else:
            return {"error": "No results found."}, 404
