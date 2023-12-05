from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class VoteSchema(Schema):
    up = fields.Integer()
    down = fields.Integer()


class CommentSchema(Schema):
    id = fields.String(dump_only=True)
    post_id = fields.String()
    author = fields.String(dump_only=True)
    content = fields.String(required=True)
    vote = fields.Nested(VoteSchema, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    class Meta:
        exclude = ["deleted_at", "created_at", "updated_at"]


comment_schema = CommentSchema()
