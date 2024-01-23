from flask_restful import Resource, request, current_app
from app.models.post import PostModel
from app.schemas.post import post_schema


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
                sort_values.append({"vote": 1})
            else:
                sort_values.append({"vote": -1})
        if sort_date.lower() == "asc":
            sort_values.append({"created_at": 1})
        else:
            sort_values.append({"created_at": -1})

        skip = (page - 1) * limit

        pipeline = [
            {"$match": {"deleted_at": None}},
            {
                "$lookup": {
                    "from": "user_model",
                    "localField": "author",
                    "foreignField": "_id",
                    "as": "author",
                }
            },
            {"$unwind": "$author"},
            {
                "$project": {
                    "id": "$_id",
                    "title": 1,
                    "content": {"$concat": [{"$substr": ["$content", 0, 200]}, "..."]},
                    "url": 1,
                    "vote": 1,
                    "created_at": 1,
                    "updated_at": 1,
                    "author": {"id": "$author._id", "name": "$author.name"},
                }
            },
        ]

        if sort_values:
            sort_dict = {}
            for sort_value in sort_values:
                sort_dict.update(sort_value)
            pipeline.append({"$sort": sort_dict})

        pipeline.append({"$skip": skip})
        pipeline.append({"$limit": limit})

        cursor = PostModel.objects().aggregate(
            [
                {"$facet": {"results": pipeline, "count": [{"$count": "total"}]}},
            ]
        )

        query_result = next(cursor, None)

        if query_result:
            results = query_result.get("results", [])
            try:
                total_count = query_result.get("count", [{}])[0].get("total", 0)
            except:
                total_count = 0

            total_pages = (total_count + limit - 1) // limit
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
