from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class TagSchema(Schema):
    id = fields.String(dump_only=True)
    author = fields.String(dump_only=True)
    name = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    class Meta:
        exclude = ["deleted_at"]


tag_schema = TagSchema()
