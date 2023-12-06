from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class CommentSchema(Schema):
    id = fields.String(dump_only=True)
    post_id = fields.String()
    author = fields.String(dump_only=True)
    content = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    class Meta:
        exclude = ["deleted_at", "created_at", "updated_at"]


comment_schema = CommentSchema()
