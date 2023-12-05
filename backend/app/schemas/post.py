from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class VoteEmbeddedSchema(Schema):
    up = fields.Int(required=True, default=0, validate=lambda x: x >= 0)
    down = fields.Int(required=True, default=0, validate=lambda x: x >= 0)


class CommentEmbeddedSchema(Schema):
    author = fields.String(required=True)
    content = fields.String(required=True, max_length=1024)
    vote = fields.Nested(VoteEmbeddedSchema, default={})


class PostSchema(Schema):
    id = fields.String()
    title = fields.String(required=True)
    author = fields.String(required=True, dump_only=True)
    content = fields.String(required=True)
    vote = fields.Nested(VoteEmbeddedSchema, default={})
    comments = fields.Nested(CommentEmbeddedSchema, many=True)
    url = fields.String(required=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    class Meta:
        exclude = ["deleted_at"]


post_schema = PostSchema()
