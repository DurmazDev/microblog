from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class AuthorEmbeddedSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True)
    vote = fields.Integer(dump_only=True, allow_none=True)


class CommentEmbeddedSchema(Schema):
    id = fields.String(dump_only=True)
    author = fields.Nested(AuthorEmbeddedSchema)
    content = fields.String(required=True, max_length=1024)
    vote = fields.Integer(required=True, dump_only=True)
    created_at = fields.String(dump_only=True)  # fields.DateTime(dump_only=True)


class TagEmbeddedSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(dump_only=True)


class PostSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True)
    author = fields.Nested(AuthorEmbeddedSchema)
    content = fields.String(required=True)
    tags = fields.Nested(TagEmbeddedSchema, many=True)
    vote = fields.Integer(dump_only=True)
    comments = fields.Nested(CommentEmbeddedSchema, many=True)
    url = fields.String(required=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    class Meta:
        exclude = ["deleted_at"]


post_schema = PostSchema()
