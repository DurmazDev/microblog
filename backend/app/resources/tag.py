from flask_restful import Resource, request
from bson import ObjectId

from app.middleware.auth import auth_required
from app.models.tag import TagModel
from app.schemas.tag import tag_schema


class TagResource(Resource):
    """
    Endpoint:
        GET /tag
        GET /tag/<id>
        POST /tag
        PUT /tag/<id>
        DELETE /tag/<id>
    """

    def get(self, id=None):
        """
        Lists the tags.

        Parameters:
            id (ObjectId, optional): Tag ID Value

        Returns:
            JSON: List of tags with pagination as JSON
        """
        if id is None:
            tags = TagModel.objects.filter(deleted_at=None)
        else:
            tags = TagModel.objects(id=id, deleted_at=None).get()

        if tags is None or len(list(tags)) == 0:
            return {"error": "Tags not found."}, 404
        else:
            if type(tags) == TagModel:
                return tag_schema.dump(tags), 200
            return tag_schema.dump(tags, many=True), 200

    @auth_required
    def post(self):
        """
        Creates a new tag on a post.

        Returns:
            JSON: Message indicating successful tag creation or error message
        """
        values = request.get_json()
        errors = tag_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        tag_name = str(values["name"]).lower().capitalize()

        try:
            current_tag = TagModel.objects(name=tag_name, deleted_at=None).get()
            if current_tag is not None:
                return {
                    "id": str(current_tag.id),
                    "name": current_tag.name,
                    "message": "This tag already exists.",
                }, 409
        except TagModel.DoesNotExist:
            pass

        created_tag = TagModel.objects.create(name=tag_name, author=request.user["id"])
        return {
            "id": str(created_tag.id),
            "name": created_tag.name,
            "message": "Tag successfully created.",
        }, 201

    @auth_required
    def put(self, id):
        """
        Updates an existing tag.

        Parameters:
            id (ObjectId): Tag ID Value

        Returns:
            JSON: Updated tag as JSON or error message
        """
        values = request.get_json()
        errors = tag_schema.validate(values)
        if errors:
            return {"error": "Unallowed attribute."}, 400

        data = tag_schema.load(values)
        try:
            tag = TagModel.objects(id=id).get()
            if tag.author != ObjectId(request.user["id"]):
                return {"error": "You are not authorized for this event."}, 401
        except TagModel.DoesNotExist:
            return {"error": "Tag not found."}, 404

        tag.name = data["name"]
        tag.save()
        return tag_schema.dump(tag), 200

    @auth_required
    def delete(self, id):
        """
        Deletes a tag & update post tags.

        Parameters:
            id (ObjectId): Tag ID Value

        Returns:
            int: HTTP status code 204 for successful deletion or error message
        """
        try:
            tag = TagModel.objects(id=id, deleted_at=None).get()
            if tag.author != ObjectId(request.user["id"]):
                return {"error": "You are not authorized for this event."}, 401
        except TagModel.DoesNotExist:
            return {}, 204

        # TODO(ahmet): Update post tags when a tag is deleted

        tag.soft_delete()
        return {}, 204
