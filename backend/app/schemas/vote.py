from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class VoteSchema(Schema):
    id = fields.String(dump_only=True)
    author = fields.String(dump_only=True)
    post_id = fields.String()
    vote_value = fields.Integer()


vote_schema = VoteSchema()
