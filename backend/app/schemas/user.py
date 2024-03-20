from marshmallow import Schema, fields
from bson import ObjectId

Schema.TYPE_MAPPING[ObjectId] = fields.String()


class UserSchema(Schema):
    id = fields.String()
    name = fields.String()
    email = fields.Email()
    password = fields.String(load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    def load(self, data, *args, **kwargs):
        data.pop("password", None)
        return super(UserSchema, self).load(data, *args, **kwargs)

    class Meta:
        exclude = ["deleted_at", "created_at", "updated_at"]


user_schema = UserSchema()


class SimpleUserSchema(Schema):
    id = fields.String()
    name = fields.String()


class UserFollowSchema(Schema):
    id = fields.String(dump_only=True)
    follower_id = fields.String(dump_only=True, required=False, allow_none=True)
    followee_id = fields.String(required=True)
    followee = fields.Nested(
        SimpleUserSchema, dump_only=True, required=False, allow_none=True
    )
    follower = fields.Nested(
        SimpleUserSchema, dump_only=True, required=False, allow_none=True
    )
    name = fields.String(dump_only=True, allow_none=True, required=False)
    created_at = fields.DateTime(dump_only=True)
    deleted_at = fields.DateTime(dump_only=True)

    class Meta:
        exclude = ["deleted_at", "created_at"]


user_follow_schema = UserFollowSchema()
