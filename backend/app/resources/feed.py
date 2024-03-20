from flask_restful import Resource, request
from app.models.post import PostModel
from app.models.user import UserModel, UserFollowModel
from app.models.tag import TagModel
from app.schemas.post import PostSchema
from app.models.tag import TagModel
from app.middleware.auth import check_token


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
        sort_tag = request.args.get("tag", None, type=str)
        followed_only = request.args.get("q", None, type=str)

        sort_values = []

        if sort_vote:
            if sort_vote.lower() == "asc":
                sort_values.append("vote")
            else:
                sort_values.append("-vote")
        if sort_date:
            if sort_date.lower() == "asc":
                sort_values.append("created_at")
            else:
                sort_values.append("-created_at")

        skip = (page - 1) * limit
        if followed_only == "followed" and check_token(request) == True:
            followed_users = UserFollowModel.objects.filter(
                follower_id=request.user["id"]
            ).only("followee_id")

            if len(followed_users) == 0:
                results = (
                    PostModel.objects(deleted_at=None)
                    .skip(skip)
                    .limit(limit)
                    .order_by(*sort_values)
                )
            else:
                followed_users = [followed.followee_id for followed in followed_users]
                results = (
                    PostModel.objects(author__in=followed_users, deleted_at=None)
                    .skip(skip)
                    .limit(limit)
                    .order_by(*sort_values)
                )
        else:
            results = (
                PostModel.objects(deleted_at=None)
                .skip(skip)
                .limit(limit)
                .order_by(*sort_values)
            )

        author_ids = [post["author"] for post in results]
        author_data = UserModel.objects(id__in=author_ids).only("id", "name")
        author_data_map = {author.id: author.name for author in author_data}

        for post in results:
            author_id = post["author"]
            author_name = author_data_map.get(author_id, "Anonymous")
            post["author"] = {"id": author_id, "name": author_name}

        nested_tag_ids = [post["tags"] for post in results]
        tag_ids = []
        [tag_ids.extend(inner_list) for inner_list in nested_tag_ids]
        tag_data = TagModel.objects(id__in=tag_ids).only("id", "name")
        tag_data_map = {tag["id"]: tag["name"] for tag in tag_data}

        if sort_tag and sort_tag in tag_data_map.values():
            new_results = []
            outher_results = []
            for post in results:
                if sort_tag in [tag_data_map[tag] for tag in post["tags"]]:
                    new_results.append(post)
                else:
                    outher_results.append(post)
            results = new_results + outher_results

        for post in results:
            post_tag_ids = post["tags"]
            temp_tags = []
            for id in post_tag_ids:
                tag_name = tag_data_map.get(id, "Unknown")
                temp_tags.append({"id": id, "name": tag_name})
            post["tags"] = temp_tags

        total_count = PostModel.objects(deleted_at=None).count()
        total_pages = (total_count + limit - 1) // limit

        feed_schema = PostSchema(exclude=("deleted_at", "comments"))

        if results:
            return {
                "results": feed_schema.dump(results, many=True),
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
